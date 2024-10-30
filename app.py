import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Punto de Equilibrio - WSE", layout="wide")
st.title("Punto de Equilibrio - WSE")

# Create two columns
col1, col2 = st.columns(2)

#-------------------------------#
#---(1) User Inputs------------#
#-------------------------------#

with col1:
    # Basic Inputs
    cantidad = st.number_input("Cantidad", min_value=0, value=30)
    precio = st.number_input("Precio unitario", min_value=0.0, value=3800.0, format="%.2f")

    # Variable Costs
    st.markdown("<u>Descripción de costos variables</u>", unsafe_allow_html=True) 
    data1 = {
        "DESCRIPCIÓN": [
            "COMBUSTIBLE NACIONAL", "COMBUSTIBLE INTERNACIONAL", "VIATICOS NACIONALES", 
            "VIATICOS INTERNACIONAL", "PEAJES NACIONALES 1", "PEAJES NACIONALES 2",
            "GASTOS NACIONALES", "GASTOS INTERNACIONALES"
        ],
        "VALOR": [1100.0, 729.0, 13.33, 30.0, 148.46, 121.28, 15.0, 30.0],
        "CANTIDAD": [1, 1, 5, 4, 1, 1, 1, 1],
    }
    
    df1 = pd.DataFrame(data1)

    # Display editable table for VALOR and CANTIDAD
    edited_df1 = st.data_editor(df1[['DESCRIPCIÓN', 'VALOR', 'CANTIDAD']], use_container_width=True, num_rows="dynamic")

    # Calculate "IMPORTE" based on edited values
    edited_df1['IMPORTE'] = edited_df1['VALOR'] * edited_df1['CANTIDAD']

    # Display updated table with IMPORTE
    #st.write("Tabla actualizada con el cálculo de 'IMPORTE'")
    #st.dataframe(edited_df1)

    variable_cost = edited_df1['IMPORTE'].sum()
    st.number_input("Costos variable unitario", min_value=0.0, value=variable_cost, format="%.2f", disabled=True)

    # Fixed Costs
    st.markdown("<u>Descripción de costos fijos</u>", unsafe_allow_html=True) 
    data2 = {
        "DESCRIPCIÓN": [
            "SUELDOS", "ALQUILER DEL LOCAL", "REPARACIÓN Y MANTENIMINETO", "INTERNET", 
            "CELULAR", "AGUA", "ELECTRICIDAD", "MATERIALES Y ÚTILES DE OFICINA",
            "MOVILIDAD", "DEPRECIACIÓN", "GASTOS FINANCIEROS", "SEGUROS", "OTROS GPS"
        ],
        "IMPORTE": [13750.0, 6750.0, 3750.0, 125.0, 300.0, 162.5, 175.0, 50.0, 1625.0, 15625.0, 23750.0, 3750.0, 550.0]
    }
    df2 = pd.DataFrame(data2)

    edited_df2 = st.data_editor(df2, use_container_width=True, num_rows="dynamic")  # Editable fixed cost table
    fixed_cost = edited_df2['IMPORTE'].sum()  # Calculate total fixed cost
    st.number_input("Costos fijos", min_value=0.0, value=fixed_cost, format="%.2f", disabled=True)  # Display final fixed cost

#-------------------------------#
#---(2) Results-----------------#
#-------------------------------#

with col2:
    num_tablas = st.number_input("Filas", min_value=1, value=10)
    step = st.number_input("Saltos", min_value=1, value=5)

    # Calculate sales, costs, and benefits based on current values
    q_values = [step * i for i in range(1, num_tablas + 1)]
    ventas = [q * precio for q in q_values]
    costos = [fixed_cost + q * variable_cost for q in q_values]
    beneficios = [v - c for v, c in zip(ventas, costos)]

    # Create results table
    resultados_df = pd.DataFrame({
        "q": q_values,
        "Ventas": ventas,
        "Costos": costos,
        "Beneficio": beneficios
    })

    st.dataframe(resultados_df)

    #---Graph---#
    plt.figure(figsize=(10, 6))
    plt.plot(q_values, ventas, label='Ventas', color='blue')
    plt.plot(q_values, costos, label='Costos', color='red')
    plt.plot(q_values, beneficios, label='Utilidad', color='black')

    # Find intersection point
    interseccion_x = None
    interseccion_y = None
    for i in range(len(q_values) - 1):
        if (ventas[i] >= costos[i] and ventas[i + 1] < costos[i + 1]) or (ventas[i] < costos[i] and ventas[i + 1] >= costos[i + 1]):
            interseccion_x = (q_values[i] + q_values[i + 1]) / 2
            interseccion_y = (ventas[i] + costos[i]) / 2
            break

    if interseccion_x is not None and interseccion_y is not None:
        plt.plot(interseccion_x, interseccion_y, 'ro')  # Intersection point
        plt.text(interseccion_x, interseccion_y, ' Intersección', fontsize=9, verticalalignment='bottom', horizontalalignment='right')

    plt.title('Gráfica de Ventas, Costos y Beneficios')
    plt.xlabel('Cantidad (q)')
    plt.ylabel('Valor')
    plt.legend()
    plt.grid()
    st.pyplot(plt)




# Mostrar las entradas del usuario
#st.write("### Entradas del Usuario")
#st.write(f"**Cantidad**: {cantidad}")
#st.write(f"**Precio**: {precio}")
#st.write(f"**Costo Fijo**: {costo_fijo}")
#st.write(f"**Costo Variable Total:** {variable_cost:.2f}")

# Mostrar la tabla actualizada
#st.write("### Tabla Actualizada")
#st.write(edited_df)
