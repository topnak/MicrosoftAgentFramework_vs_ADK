"""Live MAF chat demo using OpenAI Responses protocol with streaming."""

import streamlit as st


def render_live_demo():
    """Render the live MAF chat interface."""
    from live_demo.config import FOUNDRY_ENDPOINT, MODEL_DEPLOYMENT, AGENT_NAME, is_configured

    st.markdown("### 🎯 Live Demo — MAF Conversational Agent")
    st.markdown(
        "Experience the **OpenAI Responses** streaming in action. "
        "This agent can answer supply-chain questions using function tools."
    )

    if not is_configured():
        st.warning(
            "**Live demo not configured.** Create a `.env` file with:\n\n"
            "```\n"
            "FOUNDRY_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com\n"
            "FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4o\n"
            "```\n\n"
            "See `.env.example` for details.",
            icon="⚙️",
        )
        _render_mock_demo()
        return

    _render_live_chat()


def _render_mock_demo():
    """Show a simulated chat demo when Foundry is not configured."""
    st.markdown("---")
    st.markdown("#### 💬 Simulated Chat (Mock Mode)")
    st.caption("Showing what the live demo looks like. Configure `.env` for real agent responses.")

    # Mock conversation
    mock_messages = [
        {"role": "user", "content": "What is the current inventory level for SKU-4521?"},
        {
            "role": "assistant",
            "content": (
                "🔧 **Tool Call**: `query_snowflake(sku='SKU-4521')`\n\n"
                "Based on the Snowflake data, here are the current inventory levels for **SKU-4521**:\n\n"
                "| Warehouse | Quantity | Status |\n"
                "|-----------|----------|--------|\n"
                "| US-West-1 | 1,247 | ✅ In Stock |\n"
                "| US-East-1 | 834 | ✅ In Stock |\n"
                "| EU-West-1 | 156 | ⚠️ Low Stock |\n\n"
                "**Total**: 2,237 units across 3 warehouses.\n"
                "The EU-West-1 warehouse is below the reorder threshold (200 units). "
                "Would you like me to trigger a replenishment order via BlueYonder?"
            ),
        },
        {"role": "user", "content": "Yes, please reschedule delivery for EU-West-1"},
        {
            "role": "assistant",
            "content": (
                "🔧 **Tool Call**: `reschedule_delivery(order_id='ORD-EU-4521', new_date='2026-04-02')`\n\n"
                "Done! I've submitted a replenishment order through BlueYonder:\n\n"
                "- **Order ID**: ORD-EU-4521-REPL\n"
                "- **Destination**: EU-West-1 warehouse\n"
                "- **Quantity**: 500 units of SKU-4521\n"
                "- **Expected Delivery**: April 2, 2026\n"
                "- **Status**: ✅ Confirmed\n\n"
                "The order will be tracked automatically. "
                "I'll alert you if there are any delivery delays."
            ),
        },
    ]

    for msg in mock_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Interactive mock input
    if prompt := st.chat_input("Try asking a supply-chain question..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            st.markdown(
                "⚠️ **Mock mode** — configure `.env` with your Foundry endpoint "
                "to get real agent responses via the OpenAI Responses protocol."
            )


def _render_live_chat():
    """Render live chat connected to Foundry OpenAI Responses protocol."""
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    from live_demo.config import FOUNDRY_ENDPOINT, MODEL_DEPLOYMENT, AGENT_NAME

    st.markdown("---")
    st.markdown("#### 💬 Live Chat — Connected to Azure AI Foundry")

    # Initialize session state for chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "openai_client" not in st.session_state:
        try:
            project = AIProjectClient(
                endpoint=FOUNDRY_ENDPOINT,
                credential=DefaultAzureCredential(),
            )
            st.session_state.openai_client = project.get_openai_client()
            st.success("Connected to Azure AI Foundry", icon="✅")
        except Exception as e:
            st.error(f"Failed to connect: {e}")
            return

    # Display existing messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Ask your supply-chain agent..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Stream response from Foundry
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_response = ""

            try:
                stream = st.session_state.openai_client.responses.create(
                    model=MODEL_DEPLOYMENT,
                    input=prompt,
                    stream=True,
                    extra_body={
                        "agent": {
                            "name": AGENT_NAME,
                            "type": "agent_reference",
                        }
                    },
                )

                for event in stream:
                    if event.type == "response.output_text.delta":
                        full_response += event.delta
                        placeholder.markdown(full_response + "▌")

                placeholder.markdown(full_response)

            except Exception as e:
                placeholder.error(f"Error: {e}")
                full_response = f"Error: {e}"

            st.session_state.chat_messages.append(
                {"role": "assistant", "content": full_response}
            )
