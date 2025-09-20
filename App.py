import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="Iohexol Buffy Coat Separation Calculator", page_icon="🧪")
    
    st.title("🧪 Iohexol Buffy Coat Separation Calculator")
    st.markdown("""
    This calculator helps you prepare the correct volumes of iohexol and NaCl solutions 
    for perfect monocyte depletion from citrated blood, based on the research by:
    
    *Bøyum et al. Scandinavian Journal of Immunology 56(1):76-84 (2002)*
    """)
    
    st.header("Input Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        blood_volume = st.number_input("Volume of citrated whole blood (mL)", 
                                      min_value=1.0, value=10.0, step=1.0)
        iohexol_concentration = st.selectbox("Concentration of your iohexol", 
                                           options=["240 mgI/mL", "300 mgI/mL", "350 mgI/mL"], 
                                           index=2)
    
    with col2:
        sample_type = st.radio("Type of sample", 
                              options=["Buffy coat (stored)", "Fresh whole blood"], 
                              index=0)
        nacl_concentration = st.selectbox("NaCl solution available", 
                                        options=["0.8%", "0.9%", "1.0%", "Custom"], 
                                        index=1)
    
    if nacl_concentration == "Custom":
        custom_nacl = st.number_input("Enter custom NaCl concentration (%)", 
                                     min_value=0.1, value=0.9, step=0.1)
    else:
        custom_nacl = float(nacl_concentration.strip('%'))
    
    # Calculations
    if sample_type == "Buffy coat (stored)":
        target_osmolality = 300  # mOsm/kg
        nacl_percent = 0.9
    else:
        target_osmolality = 315  # mOsm/kg
        nacl_percent = 1.0
    
    # Convert iohexol concentration to numeric value
    iohexol_conc_value = float(iohexol_concentration.split(' ')[0])
    
    # Calculate volumes
    dilution_factor = 1.0  # For making 30% stock from pure iohexol
    if iohexol_conc_value == 350:
        dilution_factor = 1.0  # 1:1 dilution for 350 -> ~30%
    elif iohexol_conc_value == 300:
        dilution_factor = 0.86  # Different dilution needed
    
    # Calculate volumes needed
    final_medium_volume = 0.75 * blood_volume  # mL of separation medium needed
    
    # For the 30% stock solution
    stock_volume_needed = (40 / 83.66) * final_medium_volume
    nacl_volume_needed = (43.66 / 83.66) * final_medium_volume
    
    # For making the 30% stock from pure iohexol
    pure_iohexol_needed = stock_volume_needed / 2
    water_needed = stock_volume_needed / 2
    
    # For blood preparation
    blood_dilution_volume = blood_volume  # equal volume of NaCl for 1:1 dilution
    
    st.header("Results")
    
    st.success(f"For **{blood_volume} mL** of {'buffy coat' if sample_type == 'Buffy coat (stored)' else 'fresh whole blood'}, you will need:")
    
    # Display results in a table
    results_data = {
        "Step": [
            "Prepare 30% iohexol stock solution",
            "Prepare separation medium",
            "Prepare blood sample",
            "Total materials needed"
        ],
        "Components": [
            f"{pure_iohexol_needed:.2f} mL pure iohexol + {water_needed:.2f} mL water",
            f"{stock_volume_needed:.2f} mL 30% stock + {nacl_volume_needed:.2f} mL {nacl_percent}% NaCl",
            f"{blood_volume:.2f} mL blood + {blood_dilution_volume:.2f} mL 0.9% NaCl",
            ""
        ],
        "Total Volume": [
            f"{stock_volume_needed:.2f} mL",
            f"{final_medium_volume:.2f} mL",
            f"{blood_volume + blood_dilution_volume:.2f} mL",
            ""
        ]
    }
    
    results_df = pd.DataFrame(results_data)
    st.table(results_df)
    
    st.subheader("Protocol Summary")
    
    st.markdown(f"""
    1. **Prepare 30% iohexol stock**:
       - Mix {pure_iohexol_needed:.2f} mL of your {iohexol_concentration} iohexol with {water_needed:.2f} mL distilled water
    
    2. **Prepare separation medium**:
       - Mix {stock_volume_needed:.2f} mL of the 30% iohexol stock with {nacl_volume_needed:.2f} mL of {nacl_percent}% NaCl
       - This will give you {final_medium_volume:.2f} mL of separation medium (density: 1.075 g/mL, osmolality: {target_osmolality} mOsm/kg)
    
    3. **Prepare blood sample**:
       - Dilute {blood_volume:.2f} mL of citrated blood with {blood_dilution_volume:.2f} mL of 0.9% NaCl
    
    4. **Centrifugation**:
       - In a centrifuge tube, layer {final_medium_volume:.2f} mL separation medium beneath {blood_volume + blood_dilution_volume:.2f} mL diluted blood
       - Centrifuge at 700 × g for 17 minutes at room temperature
       
    5. **Harvest**:
       - Collect the lymphocyte band at the interface
    """)
    
    st.info("""
    **Important Notes:**
    - This protocol only works with **citrated** blood (ACD or CPD anticoagulant)
    - It will not work with EDTA or Heparin anticoagulants
    - For best results, verify the density of your final separation medium with a densitometer
    - All materials should be at room temperature before starting
    """)

if __name__ == "__main__":
    main()
