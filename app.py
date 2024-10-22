import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Punto de Equilibrio - WSE", layout="wide")
st.title("Punto de Equilibrio - WSE")

# Crear dos columnas
col1, col2 = st.columns(2)

#-------------------------------#
#---(1) Inputs del usuario------#
#-------------------------------#

with col1:
    #---Inputs básicos---#
    cantidad = st.number_input("Cantidad", min_value=0, value=30)
    precio = st.number_input("Precio unitario", min_value=0.0, value=3800.0, format="%.2f")

    #---Costos Variables---#
    st.markdown("<u>Descripción de costos variables</u>", unsafe_allow_html=True) 
    data1 = {
        "DESCRIPCIÓN": [
            "COMBUSTIBLE NACIONAL", "COMBUSTIBLE INTERNACIONAL", "VIATICOS NACIONALES", 
            "VIATICOS INTERNACIONAL", "PEAJES NACIONALES 1", "PEAJES NACIONALES 2",
            "GASTOS NACIONALES", "GASTOS INTERNACIONALES"
        ],
        "VALOR": [1100.0, 729.0, 13.33, 30.0, 148.46, 121.28, 15.0, 30.0],
        "CANTIDAD": [1, 1, 5, 4, 1, 1, 1, 1],
        "IMPORTE": [1100.0, 729.0, 66.67, 120.0, 148.46, 121.28, 15.0, 30.0]
    }
    df1 = pd.DataFrame(data1)

    edited_df1 = st.data_editor(df1, use_container_width=True, num_rows="dynamic")  #Mostrar la tabla editable
    variable_cost = edited_df1["IMPORTE"].sum() #Calculo del CV
    cv_totales = st.number_input("Costos variable unitario", min_value=0.0, value=variable_cost, format="%.2f", disabled=False) #Mostrar celda del CV final

    #---Costos Fijos---#
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

    edited_df2 = st.data_editor(df2, use_container_width=True, num_rows="dynamic")  #Mostrar la tabla editable
    fixed_cost = edited_df2["IMPORTE"].sum() #Calculo del CF
    cf_totales = st.number_input("Costos fijos", min_value=0.0, value=fixed_cost, format="%.2f", disabled=False) #Mostrar celda del CF final

#-------------------------------#
#---(2) Resultados--------------#
#-------------------------------#

with col2:
    #st.markdown("### Resultados")

    #Rango y steps
    num_tablas = st.number_input("Filas", min_value=1, value=10)
    step = st.number_input("Saltos", min_value=1, value=5)

    #Tabla
    q_values = [step * i for i in range(1, num_tablas + 1)]
    ventas = [q * precio for q in q_values]
    costos = [fixed_cost + q * variable_cost for q in q_values]
    beneficios = [v - c for v, c in zip(ventas, costos)]

    resultados_df = pd.DataFrame({
        "q": q_values,
        "Ventas": ventas,
        "Costos": costos,
        "Beneficio": beneficios
    })

    st.dataframe(resultados_df)

    #---Gráfica---#
    #st.markdown("### Gáfico ventas, costos, utilidad")

    plt.figure(figsize=(10, 6))
    plt.plot(q_values, ventas, label='Ventas', color='blue')
    plt.plot(q_values, costos, label='Costos', color='red')
    plt.plot(q_values, beneficios, label='Utilidad', color='black')

    # Encontrar el punto de intersección entre Costos y Ventas
    interseccion_x = None
    interseccion_y = None
    for i in range(len(q_values) - 1):
        if (ventas[i] >= costos[i] and ventas[i + 1] < costos[i + 1]) or (ventas[i] < costos[i] and ventas[i + 1] >= costos[i + 1]):
            interseccion_x = (q_values[i] + q_values[i + 1]) / 2
            interseccion_y = (ventas[i] + costos[i]) / 2
            break

    if interseccion_x is not None and interseccion_y is not None:
        plt.plot(interseccion_x, interseccion_y, 'ro')  # Punto de intersección
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
