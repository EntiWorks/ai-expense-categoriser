import streamlit as st
import requests
import altair as alt
import pandas as pd

# Initialise history in session state
if "history" not in st.session_state:
    st.session_state.history = []

st.set_page_config(page_title="AI Expense Categoriser", page_icon="💸")

st.title("💸 AI Expense Categoriser")
st.write("Enter a transaction description and let the model categorise it.")

description = st.text_input("Transaction Description", "")

if st.button("Categorise"):
    if description.strip() == "":
        st.warning("Please enter a description first.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/categorise",
            json={"description": description}
        )

        if response.status_code == 200:
            data = response.json()
            category = data["category"]
            confidence = data["confidence"]
            all_conf = data["all_confidences"]

            st.success(f"Predicted Category: **{category}**")
            st.write(f"Confidence: **{confidence:.2f}**")

            # Convert dict → DataFrame
            df_probs = pd.DataFrame({
                "Category": list(all_conf.keys()),
                "Probability": list(all_conf.values())
            })

            # Add colour: highlight predicted category
            df_probs["Colour"] = df_probs["Category"].apply(
                lambda c: "Predicted" if c == category else "Other"
            )

            # Altair bar chart
            chart = (
                alt.Chart(df_probs)
                .mark_bar()
                .encode(
                    x=alt.X("Category:N", sort="-y"),
                    y=alt.Y("Probability:Q"),
                    color=alt.Color(
                        "Colour:N",
                        scale=alt.Scale(
                            domain=["Predicted", "Other"],
                            range=["#4CAF50", "#90CAF9"]
                        ),
                        legend=None
                    ),
                    tooltip=["Category:N", "Probability:Q"]
                )
                .properties(height=300)
            )

            st.subheader("Category Probabilities")
            st.altair_chart(chart, use_container_width=True)

            with st.expander("Raw probability values"):
                st.json(all_conf)

            # Add to prediction history
            st.session_state.history.append({
                "Description": description,
                "Predicted Category": category,
                "Confidence": round(confidence, 3)
            })

        else:
            st.error("Error contacting the API.")

# Prediction history table
st.subheader("Prediction History")

if len(st.session_state.history) > 0:
    st.dataframe(st.session_state.history)
else:
    st.write("No predictions yet.")

    
# -------------------------
# Batch CSV Upload
# -------------------------

st.header("📂 Batch CSV Upload")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "description" not in df.columns:
        st.error("CSV must contain a 'description' column.")
    else:
        st.write("Preview of uploaded data:")
        st.dataframe(df.head())

        if st.button("Process CSV"):
            results = []

            for desc in df["description"]:
                response = requests.post(
                    "http://127.0.0.1:8000/categorise",
                    json={"description": desc}
                )

                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        "Description": desc,
                        "Predicted Category": data["category"],
                        "Confidence": round(data["confidence"], 3)
                    })
                else:
                    results.append({
                        "Description": desc,
                        "Predicted Category": "ERROR",
                        "Confidence": 0
                    })

            results_df = pd.DataFrame(results)

            st.subheader("Batch Results")
            st.dataframe(results_df)

            # -------------------------
            # Category Distribution Chart (FULLY FIXED)
            # -------------------------

            st.subheader("Category Distribution")

            # Build distribution safely
            dist_df = pd.DataFrame(
                results_df["Predicted Category"].value_counts()
            ).reset_index()

            # Force correct column names
            dist_df.columns = ["Category", "Count"]

            # Ensure correct types
            dist_df["Category"] = dist_df["Category"].astype(str)
            dist_df["Count"] = dist_df["Count"].astype(int)

            # Build chart
            dist_chart = (
                alt.Chart(dist_df)
                .mark_bar()
                .encode(
                    x=alt.X("Category:N", sort="-y"),
                    y=alt.Y("Count:Q"),
                    color=alt.Color(
                        "Category:N",
                        scale=alt.Scale(scheme="tableau20")
                    ),
                    tooltip=["Category:N", "Count:Q"]
                )
                .properties(height=300)
            )

            st.altair_chart(dist_chart, use_container_width=True)
