import streamlit as st

def main():
    st.title("Calculadora Insulina")

    col_1, col_2, col_3 = st.columns(3)

    with col_1:
        st.session_state["glicemia"] = st.radio("Glicemia", ["estável", "ascendente", "descendente"])
    with col_2:
        st.session_state["alimento"] = st.selectbox("Alimento", ["maçã", "banana", "laranja"])
    with col_3:
        st.session_state["quantidade"] = st.number_input("Quantidade (g)", value=50, step=1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


