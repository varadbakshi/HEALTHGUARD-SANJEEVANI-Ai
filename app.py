# ----------------------------------------------------------------------
# PART 1/3: Setup, Styling, Model Loading, Helper Functions
# ----------------------------------------------------------------------
# HEALTHGUARD - Disease Prediction and Holistic Remedy Companion
# ----------------------------------------------------------------------
# --- IMPORTS ---
# ----------------------------------------------------------------------
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from geopy.distance import geodesic
import base64
import os
import re # Import regular expressions for formatting

# ----------------------------------------------------------------------
# --- PAGE CONFIGURATION ---
# ----------------------------------------------------------------------
st.set_page_config( page_title="HealthGuard - Sanjeevani", page_icon="🌿", layout="wide", initial_sidebar_state="expanded" )

# ----------------------------------------------------------------------
# --- BACKGROUND IMAGE & STYLING ---
# ----------------------------------------------------------------------
@st.cache_data


def apply_styling():
    """Applies CSS styling for background and element visibility."""
   

    # <<< COMPLETE CSS BLOCK >>>
    page_css = f"""
    <style>
    /* --- Main Background --- */
 [data-testid="stAppViewContainer"] > .main {{ background-size: cover; background-position: center center; background-repeat: no-repeat; background-attachment: fixed; }}
    [data-testid="stAppViewContainer"] > .main:before {{ content: ""; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background-color: #e0e0e0; z-index: -2; }}
    [data-testid="stAppViewContainer"] > .main > div {{ z-index: 1; }}

    /* --- Sidebar Styling --- */
    [data-testid="stSidebar"] > div:first-child {{ background-color: rgba(240, 248, 255, 0.92); border-radius: 8px; border-right: 1px solid #ccc; }}
    [data-testid="stSidebar"] .menu-title, [data-testid="stSidebar"] h2 {{ color: #004080 !important; font-weight: bold !important; text-shadow: none !important; padding-top: 15px; padding-bottom: 10px; text-align: center; }}
    [data-testid="stSidebar"] .menu-icon {{ color: #004080 !important; }}
    [data-testid="stSidebarNav"] .nav-link {{ font-size: 16px; text-align: left; margin: 5px; border-radius: 5px; transition: background-color 0.3s, color 0.3s; }}
    [data-testid="stSidebarNav"] .nav-link:hover {{ background-color: #e1f5fe; color: #01579b; }}
    [data-testid="stSidebarNav"] .nav-link-selected {{ background-color: #007bff; color: white; font-weight: bold; }}
    [data-testid="stSidebarNav"] .nav-link.nav-link-selected:hover {{ background-color: #0056b3; color: white; }}
    /* --- Main Content Text Visibility --- */
       h1, h2 {{ color: black }}
    h3, h4, h5, h6 {{ color: #000000 }}
    .stTextInput label, .stSelectbox label, .stNumberInput label {{ color: #cfcfcf !important;  font-weight: bold !important; font-size: 1.05em; }}
    /* <<< UPDATED General Text Color >>> */
    p, .stMarkdown p, .stCaption, .stText {{
        color: #000000; /* Changed to white for better contrast */
        line-height: 1.6;
    }}
    .stTextInput [data-baseweb="input"] input::placeholder {{ color: cfcfcf !important; }}
    /* Keep input text dark on light background */
    .stTextInput input, .stNumberInput input {{ color: #333 !important; background-color: rgba(224, 224, 224, 0.9); }}

    /* --- Component Styling --- */
    div[data-testid="stButton"] > button {{
        border: 2px solid #ffffff !important;  /* White border */
        border-radius: 20px !important;
        padding: 10px 24px !important;
        font-weight: bold !important;
        transition: background-color 0.3s, transform 0.1s, box-shadow 0.3s !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        transform: scale(1.05) !important; /* Slightly more pop */
        box-shadow: 0 4px 8px rgba(0,0,0,0.4) !important;
    }}

    /* Primary Prediction Button */
    div[data-testid="stButton"] > button[kind="primary"] {{
        background-color: #0B5345 !important; /* Dark Green Background */
        color: white !important;
        border-color: #A2D9CE !important; /* Lighter contrasting border */
    }}
     div[data-testid="stButton"] > button[kind="primary"]:hover {{
        background-color: #07382d !important;
        border-color: #F0FFF0 !important;
    }}

     /* Secondary Search Button */
    div[data-testid="stButton"] > button:not([kind="primary"]) {{
        background-color: #e6f0ff !important; /* Lighter Blue background */
        color: 2px solid #000000 !important; /* Darker Blue text */
        border-color: #004080 !important;
    }}
    div[data-testid="stButton"] > button:not([kind="primary"]):hover {{
        background-color: #cce0ff !important; /* Slightly darker blue on hover */
        border-color: #002040 !important;
        color: #002040 !important;
    }}

    /* Notifications */
    [data-testid="stNotification"] {{ border-radius: 8px; border: 1px solid #a0a0a0; text-shadow: none; font-size: 1.05em; margin-top: 10px; margin-bottom: 10px; }}
    [data-testid="stNotificationSuccess"] {{ background-color: rgba(212, 237, 218, 0.97); color: #155724; border-color: #c3e6cb; }}
    [data-testid="stNotificationWarning"] {{ background-color: rgba(255, 243, 205, 0.97); color: #856404; border-color: #ffeeba; }}
    [data-testid="stNotificationError"] {{ background-color: rgba(248, 215, 218, 0.97); color: #721c24; border-color: #f5c6cb; }}

    /* Doctor Result Styling */
    .stMarkdown small {{ color: #000000 !important; line-height: 1.4; }}
    .stMarkdown a {{ color: #90CAF9 !important; text-decoration: none !important; font-weight: bold; }}
    .stMarkdown a:hover {{ color: #BBDEFB !important; text-decoration: underline !important; }}
    div[data-testid="stMarkdownContainer"] > p {{ margin-bottom: 1.2em; }}

    /* --- Sanjeevani Section Styling --- */
    .sanjeevani-section {{ background-color: rgba(15, 40, 15, 0.8); border-radius: 15px; padding: 25px; border: 1px solid rgba(144, 238, 144, 0.5); margin-top: 25px; margin-bottom: 25px; }}
    .sanjeevani-section h3 {{ color: #000000 !important; text-align: center; margin-bottom: 15px; font-size: 1.8em; }}
    .sanjeevani-section .stCaption {{ color: #c0e0c0 !important; text-align: center; font-style: italic; }}
    .sanjeevani-section .stExpander {{ background-color: rgba(255, 255, 255, 0.1); border-radius: 8px; margin-bottom: 12px; border: 1px solid rgba(200, 255, 200, 0.3); }}
    .sanjeevani-section .stExpander header {{ color: #D4EFDF !important; font-weight: bold; font-size: 1.25em !important; padding: 10px 0px !important; }}
    .sanjeevani-section .stExpander header svg {{ fill: #D4EFDF !important; }}

    /* <<< UPDATED Sanjeevani Inner Text & How-to >>> */
    .sanjeevani-section .stExpander div[data-testid="stExpanderDetails"] {{
        color: #000000 !important; /* Bright Text (almost white) */
        padding-left: 15px;
        font-size: 1.05em;
    }}
    /* Target paragraphs specifically for 'How:' etc. */
    .sanjeevani-section .stExpander div[data-testid="stExpanderDetails"] p {{
        color: #000000 !important;
        text-shadow: none !important; /* Remove shadow for plain text inside */
        line-height: 1.6;
        margin-bottom: 0.5em; /* Space below paragraphs */
    }}
    /* Target list items */
     .sanjeevani-section .stExpander div[data-testid="stExpanderDetails"] li {{
        color: #000000 !important;
        text-shadow: none !important;
        line-height: 1.6;
        margin-left: 1.5em; 
        margin-bottom: 0.3em;
    }}
    .sanjeevani-section .stExpander div[data-testid="stExpanderDetails"] p:has(br) {{ 
        background-color: rgba(232, 245, 233, 0.9); 
        color: #000000 !important;  /* Dark Green Text for steps */
        padding: 10px 15px;
        border-radius: 5px;
        margin-left: 5px; 
        margin-right: 5px;
        margin-bottom: 8px;
        text-shadow: none !important; 
        line-height: 1.5;
    }}
     /* Warning box inside Sanjeevani */
    .sanjeevani-section [data-testid="stNotificationWarning"] {{
         background-color: rgba(255, 229, 153, 0.85); color: #FFFFFF ; border-color: #ffecb5;
    }}
    </style>
    """
    st.markdown(page_css, unsafe_allow_html=True)

apply_styling()

# ----------------------------------------------------------------------
# --- MODEL LOADING ---
# ----------------------------------------------------------------------
@st.cache_resource
def load_model(file_path):
    """Loads a pickled model file. Handles errors."""
    try:
        with open(file_path, 'rb') as file: model = pickle.load(file); return model
    except FileNotFoundError: st.error(f"Model file not found: {file_path}."); return None
    except Exception as e: st.error(f"Error loading model {file_path}: {e}"); return None

diabetes_model = load_model('saved_models/diabetes_model.sav')
heart_disease_model = load_model('saved_models/heart_disease_model.sav')
parkinsons_model = load_model('saved_models/parkinsons_model.sav')

if not all([diabetes_model, heart_disease_model, parkinsons_model]):
    st.error("CRITICAL ERROR: One or more prediction models failed to load. Cannot continue.")
    st.stop()

# ----------------------------------------------------------------------
# --- DOCTOR / HOSPITAL DATA & HELPERS (VERIFY ALL DATA!) ---
# ----------------------------------------------------------------------
@st.cache_data
def calculate_distance(user_loc_str, doctor_location_tuple):
    """Calculates geodesic distance. Returns infinity on error."""
    try:
        if ',' not in user_loc_str: raise ValueError("Comma missing")
        user_lat, user_lon = map(float, user_loc_str.strip().split(','))
        if not (-90 <= user_lat <= 90 and -180 <= user_lon <= 180): raise ValueError("Range invalid")
        if not (isinstance(doctor_location_tuple, tuple) and len(doctor_location_tuple) == 2 and all(isinstance(coord, (int, float)) for coord in doctor_location_tuple)): raise ValueError("Invalid doctor location format")
        distance = geodesic((user_lat, user_lon), doctor_location_tuple).miles
        return distance
    except (ValueError, TypeError): return float('inf')
    except Exception as e: print(f"Error in calculate_distance: {e}"); return float('inf')

@st.cache_data
def filter_doctors(user_loc_str, _doctor_list, max_distance=30, min_rating=0.0):
    """Filters doctors by distance."""
    filtered_doctors = []
    try: # Validate user location string format first
         if ',' not in user_loc_str: raise ValueError("Comma missing")
         user_lat, user_lon = map(float, user_loc_str.strip().split(','))
         if not (-90 <= user_lat <= 90 and -180 <= user_lon <= 180): raise ValueError("Range invalid")
    except (ValueError, TypeError):
         print(f"Error: Invalid coordinate string passed to filter_doctors: {user_loc_str}")
         return [] # Return empty list if format is bad

    for doctor in _doctor_list:
        if "location" not in doctor or not isinstance(doctor["location"], tuple):
            print(f"Warning: Skipping doctor entry due to missing/invalid location: {doctor.get('name', 'Unknown')}")
            continue
        distance = calculate_distance(user_loc_str, doctor["location"])
        if distance != float('inf') and distance <= max_distance:
            filtered_doctors.append((doctor, distance))
    filtered_doctors.sort(key=lambda item: item[1]) # Sort by distance
    return filtered_doctors

def display_doctor_list(doctors):
    """Displays the filtered list of doctors/hospitals."""
    if doctors:
        st.success(f"Found {len(doctors)} options nearby (sorted by distance):")
        st.markdown("---")
        for doctor, distance in doctors: # Use single column display
            link_html = ""
            if 'link' in doctor and doctor['link'] and isinstance(doctor['link'], str) and doctor['link'].startswith('http'):
                 link_html = f" [<a href='{doctor['link']}' target='_blank'>Website/Book</a>]"
            rating_display = ""
            if 'rating' in doctor and doctor['rating'] != "N/A":
                try: rating_val = float(doctor['rating']); rating_display = f" ({rating_val:.1f} ★)"
                except (ValueError, TypeError): pass
            address = doctor.get('address', 'N/A')
            contact = doctor.get('contact', 'N/A')
            st.markdown(
                f"**{doctor['name']}** {rating_display}<br>"
                f"📍 *~{distance:.1f} miles away*{link_html}<br>"
                f"<small>Address: {address}<br>"
                f"Contact: {contact}</small><br> ",
                unsafe_allow_html=True
            )
            st.markdown("---") # Separator between entries
    else:
        st.info("No doctors/hospitals found matching your criteria within the search radius (e.g., 30 miles) from the selected city center.")

# --- CITY COORDINATES MAPPING (EXPANDED - **VERIFY THESE!**) ---
city_coordinates = {
    "Mumbai": "19.0760,72.8777", "Delhi": "28.6139,77.2090", "Bangalore": "12.9716,77.5946",
    "Chennai": "13.0827,80.2707", "Kolkata": "22.5726,88.3639", "Hyderabad": "17.3850,78.4867",
    "Pune": "18.5204,73.8567", "Ahmedabad": "23.0225,72.5714", "Jaipur": "26.9124,75.7873",
    "Lucknow": "26.8467,80.9462", "Chandigarh": "30.7333,76.7794", "Kochi": "9.9312,76.2673",
    "Nagpur": "21.1458,79.0882", "Indore": "22.7196,75.8577", "Visakhapatnam": "17.6868,83.2185",
    "Patna": "25.5941,85.1376", "Guwahati": "26.1445,91.7362", "Bhopal": "23.2599,77.4126",
    "Surat": "21.1702,72.8311", "Kanpur": "26.4499,80.3319", "Kolhapur": "16.7050,74.2433",
    "Satara": "17.6805,74.0183", "Nashik": "19.9975,73.7898"
}
sorted_cities = sorted(list(city_coordinates.keys()))

# --- DOCTOR / HOSPITAL DATA (EXPANDED & COMBINED - **VERIFY ALL DETAILS!**) ---
# Base hospital definitions (VERIFY ALL!)
kph_aster_aadhar = {"name": "Aster Aadhar Hospital", "location": (16.6966, 74.2376), "address": "2104/1A, nr Shastri Nagar Garden, Vijayanagar", "contact": "0231 2661166", "link": "https://www.asterhospitals.in/hospitals/aster-aadhar-kolhapur/book-an-appointment"}
kph_apple_saraswati = {"name": "Apple Saraswati Hospital", "location": (16.7081, 74.2446), "address": "517/A, Assembly Rd, nr Mahalaxmi temple", "contact": "0231 252 5771", "link": "https://applehospitals.com/make-an-appointment/"} # Updated Link
kph_city_hospital = {"name": "City Hospital Kolhapur", "location": (16.7080, 74.2380), "address": "308 E Ward, Venus Corner, Shahupuri", "contact": "0231 2651234", "link": "https://cityhospitalkolhapur.com/contact-us/"}
pune_ruby_hall = {"name": "Ruby Hall Clinic", "location": (18.5288, 73.8797), "address": "40, Sasoon Rd, Sangamvadi", "contact": "020 6645 5100", "link": "https://rubyhall.com/"}
pune_sahaydri_deccan = {"name": "Sahyadri Hospital Deccan", "location": (18.5172, 73.8387), "address": "Plot No. 30-C, Erandwane", "contact": "020 6721 3000", "link": "https://sahyadrihospital.com/"}
pune_jupiter = {"name": "Jupiter Hospital", "location": (18.5675, 73.9116), "address": "Baner - Pimple Nilakh Rd, Baner", "contact": "020 2799 2799", "link": "https://www.jupiterhospital.com/pune"}
pune_kims = {"name": "KEM Hospital", "location": (18.5168, 73.8720), "address": "489, Rasta Peth", "contact": "020 6603 7391", "link": "https://kempune.org/"}
satara_mangeshkar = {"name": "Shrimati Kashibai Navale Hospital (Affil.)", "location": (17.6868, 74.0181), "address": "NH4", "contact": "Verify", "link": "Verify"}
mum_kokilaben = {"name": "Kokilaben Hospital", "location": (19.1175, 72.8280), "address": "Four Bungalows, Andheri W", "contact": "022 4269 6969", "link": "https://www.kokilabenhospital.com/"}
mum_jaslok = {"name": "Jaslok Hospital", "location": (18.9618, 72.8075), "address": "15, Dr Deshmukh Marg", "contact": "022 6657 3333", "link": "https://www.jaslokhospital.net/"}
mum_lilavati = {"name": "Lilavati Hospital", "location": (19.0625, 72.8314), "address": "A-791, Bandra Reclamation", "contact": "022 2675 1000", "link": "http://www.lilavatihospital.com/"}
mum_hinduja = {"name": "P. D. Hinduja Hospital", "location": (19.0243, 72.8398), "address": "Veer Savarkar Marg, Mahim W", "contact": "022 2445 2222", "link": "https://www.hindujahospital.com/"}
nsk_apollo = {"name": "Apollo Hospitals Nashik", "location": (20.0091, 73.7699), "address": "Swaminarayan Nagar, Nr Bombay Naka", "contact": "0253 666 6100", "link": "https://nashik.apollohospitals.com/"}
nsk_wockhardt = {"name": "Wockhardt Hospitals Nashik", "location": (19.9962, 73.7671), "address": "Wadala Naka", "contact": "0253 662 4444", "link": "https://nashik.wockhardthospitals.com/"}
delhi_aiims = {"name": "AIIMS Delhi", "location": (28.5669, 77.2111), "address": "Ansari Nagar East", "contact": "011 2658 8500", "link": "https://www.aiims.edu/"}
delhi_max_saket = {"name": "Max Hospital, Saket", "location": (28.5217, 77.2132), "address": "1, Press Enclave Marg", "contact": "011 2651 5050", "link": "https://www.maxhealthcare.in/"}
delhi_fortis_vk = {"name": "Fortis Escorts Heart Institute", "location": (28.5542, 77.2704), "address": "Okhla road", "contact": "011 4713 5000", "link": "https://www.fortishealthcare.com/india/hospitals-in-delhi-ncr/fortis-escorts-heart-institute-okhla-new-delhi"}
delhi_apollo = {"name": "Indraprastha Apollo Hospitals", "location": (28.5414, 77.2818), "address": "Delhi Mathura Road", "contact": "011 7179 1090", "link": "https://delhi.apollohospitals.com/"}
blr_manipal_old = {"name": "Manipal Hospital Old Airport Rd", "location": (12.9590, 77.6490), "address": "98, HAL Old Airport Rd", "contact": "080 2502 4444", "link": "https://www.manipalhospitals.com/oldairportroad/"}
blr_fortis_bgh = {"name": "Fortis Hospital, Bannerghatta Rd", "location": (12.8770, 77.5970), "address": "154, 9, Bannerghatta Main Rd", "contact": "080 6621 4444", "link": "https://www.fortishealthcare.com/india/hospitals-in-karnataka/fortis-hospital-bannerghatta-road-bengaluru"}
blr_narayana = {"name": "Narayana Inst. Cardiac Sciences", "location": (12.8276, 77.6579), "address": "258/A, Bommasandra Ind Area", "contact": "080 7122 2222", "link": "https://www.narayanahealth.org/hospitals/bengaluru/narayana-institute-of-cardiac-sciences-bommasandra"}
blr_aster_cmi = {"name": "Aster CMI Hospital", "location": (13.0599, 77.5969), "address": "43/2, New Airport Road", "contact": "080 4342 0100", "link": "https://www.asterhospitals.in/hospitals/aster-cmi-bangalore"}
chn_apollo_greams = {"name": "Apollo Hospitals Greams Rd", "location": (13.0600, 80.2550), "address": "21, Greams Lane", "contact": "044 2829 3333", "link": "https://chennai.apollohospitals.com/"}
chn_fortis_malar = {"name": "Fortis Malar Hospital", "location": (13.0065, 80.2595), "address": "No. 52, 1st Main Rd, Adyar", "contact": "044 4289 2222", "link": "https://www.fortishealthcare.com/india/hospitals-in-chennai/fortis-malar-hospital-adyar-chennai"}
chn_kauvery = {"name": "Kauvery Hospital", "location": (13.0310, 80.2443), "address": "81, TTK Road", "contact": "044 4000 6000", "link": "https://www.kauveryhospital.com/"}
hyd_apollo_jubilee = {"name": "Apollo Hospitals Jubilee Hills", "location": (17.4200, 78.4000), "address": "Road No 72", "contact": "1860 500 1066", "link": "https://hyderabad.apollohospitals.com/"}
hyd_yashoda_som = {"name": "Yashoda Hospitals Somajiguda", "location": (17.4206, 78.4636), "address": "Raj Bhavan Road", "contact": "040 4567 4567", "link": "https://www.yashodahospitals.com/"}
hyd_care_banjara = {"name": "CARE Hospitals Banjara Hills", "location": (17.4140, 78.4510), "address": "Rd Number 1", "contact": "040 3041 8888", "link": "https://www.carehospitals.com/"}
kol_apollo_gleneagles = {"name": "Apollo Gleneagles Hospitals", "location": (22.5780, 88.4080), "address": "58, Canal Circular Rd", "contact": "033 2320 3040", "link": "https://kolkata.apollohospitals.com/"}
kol_cmri = {"name": "CMRI", "location": (22.5380, 88.3360), "address": "7, 2, Diamond Harbour Rd", "contact": "033 3090 3090", "link": "https://www.cmri.in/"}
kol_peerless = {"name": "Peerless Hospital", "location": (22.4960, 88.3890), "address": "360, Pancha Sayar Rd", "contact": "033 4011 1222", "link": "https://www.peerlesshospital.com/"}
# Add more base hospital dicts for other cities here...
ahd_apollo = {"name": "Apollo Hospitals Ahmedabad", "location": (23.0494, 72.5134), "address": "Plot No. 1A, Bhat GIDC Estate", "contact": "079 6670 1800", "link": "https://ahmedabad.apollohospitals.com/"}
kph_aster_aadhar = {"name": "Aster Aadhar Hospital", "location": (16.6966, 74.2376), "address": "2104/1A, nr Shastri Nagar Garden, Vijayanagar, Kolhapur", "contact": "0231 2661166", "link": "https://www.asterhospitals.in/hospitals/aster-aadhar-kolhapur/book-an-appointment"}
kph_apple_saraswati = {"name": "Apple Saraswati Hospital", "location": (16.7081, 74.2446), "address": "517/A, Assembly Rd, nr Mahalaxmi temple, Kolhapur", "contact": "0231 252 5771", "link": "https://applehospitals.com/make-an-appointment/"}
kph_city_hospital = {"name": "City Hospital Kolhapur", "location": (16.7080, 74.2380), "address": "308 E Ward, Venus Corner, Shahupuri, Kolhapur", "contact": "0231 2651234", "link": "https://cityhospitalkolhapur.com/contact-us/"}
pune_ruby_hall = {"name": "Ruby Hall Clinic", "location": (18.5288, 73.8797), "address": "40, Sasoon Rd, Sangamvadi, Pune", "contact": "020 6645 5100", "link": "https://rubyhall.com/appointments/"}
pune_sahaydri_deccan = {"name": "Sahyadri Hospital Deccan", "location": (18.5172, 73.8387), "address": "Plot No. 30-C, Erandwane, Pune", "contact": "020 6721 3000", "link": "https://sahyadrihospital.com/book-an-appointment/"}
pune_jupiter = {"name": "Jupiter Hospital", "location": (18.5675, 73.9116), "address": "Baner - Pimple Nilakh Rd, Baner, Pune", "contact": "020 2799 2799", "link": "https://www.jupiterhospital.com/pune/make-an-appointment"}
pune_kims = {"name": "KEM Hospital", "location": (18.5168, 73.8720), "address": "489, Rasta Peth, Pune", "contact": "020 6603 7391", "link": "https://kempune.org/hospital-services/"} # General info, might not have direct booking
satara_mangeshkar = {"name": "Shrimati Kashibai Navale Hospital (Affil.)", "location": (17.6868, 74.0181), "address": "NH4, Satara", "contact": "Verify", "link": "Verify"} # Still needs verification
satara_yashwant = {"name": "Yashwant Hospital Satara", "location": (17.6845, 73.9998), "address": "Powai Naka, Satara", "contact": "02162 235141", "link": ""} # Example, verify details & link
mum_kokilaben = {"name": "Kokilaben Hospital", "location": (19.1175, 72.8280), "address": "Four Bungalows, Andheri W, Mumbai", "contact": "022 4269 6969", "link": "https://www.kokilabenhospital.com/contacts/appointments.html"}
mum_jaslok = {"name": "Jaslok Hospital", "location": (18.9618, 72.8075), "address": "15, Dr Deshmukh Marg, Mumbai", "contact": "022 6657 3333", "link": "https://www.jaslokhospital.net/book-an-appointment"}
mum_lilavati = {"name": "Lilavati Hospital", "location": (19.0625, 72.8314), "address": "A-791, Bandra Reclamation, Mumbai", "contact": "022 2675 1000", "link": "http://www.lilavatihospital.com/content/Online-Appointments.aspx"} # Older link, verify
mum_hinduja = {"name": "P. D. Hinduja Hospital", "location": (19.0243, 72.8398), "address": "Veer Savarkar Marg, Mahim W, Mumbai", "contact": "022 2445 2222", "link": "https://www.hindujahospital.com/book-an-appointment/"}
nsk_apollo = {"name": "Apollo Hospitals Nashik", "location": (20.0091, 73.7699), "address": "Swaminarayan Nagar, Nr Bombay Naka, Nashik", "contact": "0253 666 6100", "link": "https://nashik.apollohospitals.com/book-an-appointment/"}
nsk_wockhardt = {"name": "Wockhardt Hospitals Nashik", "location": (19.9962, 73.7671), "address": "Wadala Naka, Nashik", "contact": "0253 662 4444", "link": "https://nashik.wockhardthospitals.com/make-an-appointment/"}
nsk_sixsigma = {"name": "Six Sigma Medicare & Research Ltd", "location": (19.9939, 73.7816), "address": "Near Model Colony, Nashik", "contact": "0253 231 7777", "link": "https://www.sixsigmahospital.com/"} # Example, verify details
ngp_aiims = {"name": "AIIMS Nagpur", "location": (21.0868, 79.0485), "address": "Plot No. 2, Sector-20, MIHAN", "contact": "0712-2980000", "link": "https://aiimsnagpur.edu.in/How_register_appointment"}
ngp_kingsway = {"name": "Kingsway Hospitals Nagpur", "location": (21.1544, 79.0631), "address": "44, Kingsway Rd, Mohan Nagar", "contact": "0712 678 9100", "link": "https://kingswayhospitals.com/book-an-appointment/"}
surat_kiran = {"name": "Kiran Hospital Surat", "location": (21.2096, 72.8811), "address": "Nr. Sumul Dairy, Varachha Rd", "contact": "0261 716 0000", "link": "https://kiranhospital.com/book-appointment/"}
surat_sunshine = {"name": "Sunshine Global Hospitals Surat", "location": (21.1692, 72.7900), "address": "Nr. L. P. Savani Circle, Adajan", "contact": "+91 91574 44444", "link": "https://sunshineglobalhospitals.com/book-an-appointment/"}
kanpur_regency = {"name": "Regency Hospital Kanpur", "location": (26.4720, 80.3150), "address": "A-2, Sarvodaya Nagar", "contact": "0512 350 1111", "link": "https://regencyhealthcare.in/book-an-appointment/"} # Verify link target



# --- Combined Data for Each Disease (<<< UPDATED with ALL Cities) ---
doctor_data_diabetes = [
    # KPH
    {**kph_aster_aadhar, "name": kph_aster_aadhar["name"] + " (Endocrinology)"}, {**kph_apple_saraswati, "name": kph_apple_saraswati["name"] + " (Diabetes)"}, {**kph_city_hospital, "name": kph_city_hospital["name"] + " (Diabetes)"},
    # PUNE
    {**pune_ruby_hall, "name": pune_ruby_hall["name"] + " (Endocrinology)"}, {**pune_sahaydri_deccan, "name": pune_sahaydri_deccan["name"] + " (Diabetes)"}, {**pune_jupiter, "name": pune_jupiter["name"] + " (Endocrinology)"}, {**pune_kims, "name": pune_kims["name"] + " (Gen Med/Diabetes)"},
    # MUMBAI
    {**mum_kokilaben, "name": mum_kokilaben["name"] + " (Endocrinology)"}, {**mum_hinduja, "name": mum_hinduja["name"] + " (Endocrinology)"}, {**mum_jaslok, "name": mum_jaslok["name"] + " (Diabetes)"}, {**mum_lilavati, "name": mum_lilavati["name"] + " (Diabetes)"},
    # DELHI
    {**delhi_aiims, "name": delhi_aiims["name"] + " (Endocrinology)"}, {**delhi_max_saket, "name": delhi_max_saket["name"] + " (Endocrinology)"}, {**delhi_apollo, "name": delhi_apollo["name"] + " (Endocrinology)"},
    # BANGALORE
    {**blr_manipal_old, "name": blr_manipal_old["name"] + " (Endocrinology)"}, {**blr_fortis_bgh, "name": blr_fortis_bgh["name"] + " (Endocrinology)"}, {**blr_aster_cmi, "name": blr_aster_cmi["name"] + " (Endocrinology)"},
    # CHENNAI
    {**chn_apollo_greams, "name": chn_apollo_greams["name"] + " (Endocrinology)"}, {**chn_fortis_malar, "name": chn_fortis_malar["name"] + " (Diabetes)"}, {**chn_kauvery, "name": chn_kauvery["name"] + " (Endocrinology)"},
    # HYDERABAD
    {**hyd_apollo_jubilee, "name": hyd_apollo_jubilee["name"] + " (Endocrinology)"}, {**hyd_yashoda_som, "name": hyd_yashoda_som["name"] + " (Endocrinology)"}, {**hyd_care_banjara, "name": hyd_care_banjara["name"] + " (Diabetes)"},
    # KOLKATA
    {**kol_apollo_gleneagles, "name": kol_apollo_gleneagles["name"] + " (Endocrinology)"}, {**kol_cmri, "name": kol_cmri["name"] + " (Endocrinology)"}, {**kol_peerless, "name": kol_peerless["name"] + " (Diabetes)"},
    # NASHIK
    {**nsk_apollo, "name": nsk_apollo["name"] + " (Endocrinology)"}, {**nsk_wockhardt, "name": nsk_wockhardt["name"] + " (Endocrinology)"},
    # AHMEDABAD (Example - Add others)
    {**ahd_apollo, "name": ahd_apollo["name"] + " (Endocrinology)"},
    # ... Add relevant hospital entries for Jaipur, Lucknow, Chandigarh, Kochi, Nagpur, Indore, Visakhapatnam, Patna, Guwahati, Bhopal, Surat, Kanpur ...

    # Individual Doctors (VERIFY DETAILS!)
    {"name": "Dr. Mahendra Deshmane", "location": (16.7050, 74.2433), "rating": 4.9, "address": "Rankala stand, Kolhapur", "contact": "9970916904"},
    {"name": "Dr. Rajesh Deshmane", "location": (16.7050, 74.2433), "rating": 4.8, "address": "Akshar plaza, opp sasane ground, Kolhapur", "contact": "2662345"},
    {"name": "Dr. Nikita Doshi", "location": (16.7050, 74.2433), "rating": 4.7, "address": "New Shahupuri, Kolhapur", "contact": "9529093195"},
    {"name": "Dr. Amar Raykantiwar", "location": (18.5204, 73.8567), "rating": 4.7, "address": "Dhayari Phata Chowk, Pune", "contact": "8451941050"},
    {"name": "Dr. Sarita Bhardwaj", "location": (18.5204, 73.8567), "rating": 4.9, "address": "Sasane Nagar, Hadapsar, Pune", "contact": "8087010457"},
    {"name": "Dr. Ajit More", "location": (18.5204, 73.8567), "rating": 4.8, "address": "Mhada Colony, Viman Nagar, Pune", "contact": "8761959595"},
    {"name": "Dr. Dattatray More", "location": (17.6805, 74.0183), "rating": 5.0, "address": "Degaon road, new MIDC, Satara", "contact": "8766545630"},
    {"name": "Dr. Revale's Clinic", "location": (17.6805, 74.0183), "rating": 4.8, "address": "LIC colony, Sadar Bazar, Satara", "contact": "2229052"},
    {"name": "Dr. Deepanjali Pawar", "location": (17.6805, 74.0183), "rating": 4.8, "address":"Nr ST stand, Hospital road, Parange chowk,Sadar bazar, Satara", "contact": "9503706894"},
    {"name": "Dr. Bhavik Saglani", "location": (19.0760, 72.8777), "rating": 5.0, "address": "Apollo Spectra Hospital, Tardeo, Mumbai", "contact": "9820830555"},
    {"name": "Dr. Vishal & Gupta Diabetes Endocrine center", "location": (19.0760, 72.8777), "rating": 4.3, "address": "Dhus wadi, Sonapur, Marine Lines, Mumbai", "contact": "9769327322"},
    {"name": "Dr. Shreyans Shah", "location": (19.9975, 73.7898), "rating": 4.7, "address": "Racca Colony, Nashik", "contact": "9890223465"},
    {"name": "Dr. Chaitanya Nagnath Buva", "location": (19.9975, 73.7898), "rating": 4.6, "address": "Govind Nagar, Nashik", "contact": "9673400111"},
]
doctor_data_heart = [
    # Hospitals
    {**kph_aster_aadhar, "name": kph_aster_aadhar["name"] + " (Cardiology)"}, {**kph_apple_saraswati, "name": kph_apple_saraswati["name"] + " (Cardiology)"}, {**kph_city_hospital, "name": kph_city_hospital["name"] + " (Cardiology)"},
    {**pune_ruby_hall, "name": pune_ruby_hall["name"] + " (Cardiology)"}, {**pune_sahaydri_deccan, "name": pune_sahaydri_deccan["name"] + " (Cardiology)"}, {**pune_jupiter, "name": pune_jupiter["name"] + " (Cardiology)"},
    {**mum_kokilaben, "name": mum_kokilaben["name"] + " (Cardiology)"}, {**mum_jaslok, "name": mum_jaslok["name"] + " (Cardiology)"}, {**mum_lilavati, "name": mum_lilavati["name"] + " (Cardiology)"}, {**mum_hinduja, "name": mum_hinduja["name"] + " (Cardiology)"},
    {**delhi_aiims, "name": delhi_aiims["name"] + " (Cardiology)"}, {**delhi_max_saket, "name": delhi_max_saket["name"] + " (Cardiology)"}, {**delhi_fortis_vk, "name": delhi_fortis_vk["name"]}, {**delhi_apollo, "name": delhi_apollo["name"] + " (Cardiology)"},
    {**blr_manipal_old, "name": blr_manipal_old["name"] + " (Cardiology)"}, {**blr_fortis_bgh, "name": blr_fortis_bgh["name"] + " (Cardiology)"}, {**blr_narayana, "name": blr_narayana["name"]}, {**blr_aster_cmi, "name": blr_aster_cmi["name"] + " (Cardiology)"},
    {**chn_apollo_greams, "name": chn_apollo_greams["name"] + " (Cardiology)"}, {**chn_fortis_malar, "name": chn_fortis_malar["name"] + " (Cardiology)"}, {**chn_kauvery, "name": chn_kauvery["name"] + " (Cardiology)"},
    {**hyd_apollo_jubilee, "name": hyd_apollo_jubilee["name"] + " (Cardiology)"}, {**hyd_yashoda_som, "name": hyd_yashoda_som["name"] + " (Cardiology)"}, {**hyd_care_banjara, "name": hyd_care_banjara["name"] + " (Cardiology)"},
    {**kol_apollo_gleneagles, "name": kol_apollo_gleneagles["name"] + " (Cardiology)"}, {**kol_cmri, "name": kol_cmri["name"] + " (Cardiology)"}, {**kol_peerless, "name": kol_peerless["name"] + " (Cardiology)"},
    {**nsk_apollo, "name": nsk_apollo["name"] + " (Cardiology)"}, {**nsk_wockhardt, "name": nsk_wockhardt["name"] + " (Cardiology)"},
    {**ahd_apollo, "name": ahd_apollo["name"] + " (Cardiology)"}, # Example
    # ... Add relevant hospital entries for other cities ...
    # Individual Doctors
    {"name": "Dr. Akshay Bafna", "location": (16.7050, 74.2433), "rating": 4.7, "address":"Rukmini Nagar, nr LIC ground, Kolhapur", "contact": "8767222355"},
    {"name": "Dr. Alok Shinde", "location": (16.7050, 74.2433), "rating": 5.0, "address":"Royal miraj arcade, opp railway station, Kolhapur", "contact": "7422900500"},
    {"name": "Dr. Arjun Adnaik", "location": (16.7050, 74.2433), "rating": 4.9, "address":"In front of Sayaji Hotel, Shivaji Park, Kolhapur", "contact": "2535373"},
    {"name": "Dr. Rahul Sawant", "location": (18.5204, 73.8567), "rating": 5.0, "address":"Market yard chowk, opp Hotel Utsav Deluxe, Parvati Paytha, Pune", "contact": "9021940551"},
    {"name": "Dr. Gaurav Ganeshwala", "location": (18.5204, 73.8567), "rating": 4.9, "address":"Ground Floor Ruby Hall Clinic, Sasoon Road, Pune", "contact": "8605712240"},
    {"name": "Dr. Bhushan Patil", "location": (17.6805, 74.0183), "rating": 4.9, "address":"Near Shahu Stadium, Sadar Bazaar, Satara", "contact": "9028253535"},
    {"name": "Dr. Rohit Dixit", "location": (17.6805, 74.0183), "rating": 4.8, "address":"Mane Colony, Sadar Bazaar, Satara", "contact": "2233266"},
    {"name": "Dr. Rahul Kaiche", "location": (19.9975, 73.7898), "rating": 5.0, "address": "Tilak wadi, Police Staff Colony, Nashik", "contact": "9607799333"},
    {"name": "Dr. Manoj Chopda", "location": (19.9975, 73.7898), "rating": 4.9, "address": "Yashwant Colony, Patil Colony, Canada Colony, Nashik", "contact": "9123021613"},
    {"name": "Dr. Kamales Kumar Saha", "location": (19.0760, 72.8777), "rating": 5.0, "address": "Anupam Stationary Building, Goregaon, Mumbai", "contact": "9977345555"},
    {"name": "Dr. Vijay Band", "location": (19.0625, 72.8314), "rating": 4.7, "address": "Lilavati Hospital, Bandra West, Mumbai", "contact": "50598236"},
]
doctor_data_parkinsons = [
    {**kph_aster_aadhar, "name": kph_aster_aadhar["name"] + " (Endocrinology)"}, {**kph_apple_saraswati, "name": kph_apple_saraswati["name"] + " (Diabetes)"}, {**kph_city_hospital, "name": kph_city_hospital["name"] + " (Diabetes)"},
    {**pune_ruby_hall, "name": pune_ruby_hall["name"] + " (Endocrinology)"}, {**pune_sahaydri_deccan, "name": pune_sahaydri_deccan["name"] + " (Diabetes)"}, {**pune_jupiter, "name": pune_jupiter["name"] + " (Endocrinology)"}, {**pune_kims, "name": pune_kims["name"] + " (Gen Med/Diabetes)"},
    {**mum_kokilaben, "name": mum_kokilaben["name"] + " (Endocrinology)"}, {**mum_hinduja, "name": mum_hinduja["name"] + " (Endocrinology)"}, {**mum_jaslok, "name": mum_jaslok["name"] + " (Diabetes)"}, {**mum_lilavati, "name": mum_lilavati["name"] + " (Diabetes)"},
    {**delhi_aiims, "name": delhi_aiims["name"] + " (Endocrinology)"}, {**delhi_max_saket, "name": delhi_max_saket["name"] + " (Endocrinology)"}, {**delhi_apollo, "name": delhi_apollo["name"] + " (Endocrinology)"},
    {**blr_manipal_old, "name": blr_manipal_old["name"] + " (Endocrinology)"}, {**blr_fortis_bgh, "name": blr_fortis_bgh["name"] + " (Endocrinology)"}, {**blr_aster_cmi, "name": blr_aster_cmi["name"] + " (Endocrinology)"},
    {**chn_apollo_greams, "name": chn_apollo_greams["name"] + " (Endocrinology)"}, {**chn_fortis_malar, "name": chn_fortis_malar["name"] + " (Diabetes)"}, {**chn_kauvery, "name": chn_kauvery["name"] + " (Endocrinology)"},
    {**hyd_apollo_jubilee, "name": hyd_apollo_jubilee["name"] + " (Endocrinology)"}, {**hyd_yashoda_som, "name": hyd_yashoda_som["name"] + " (Endocrinology)"}, {**hyd_care_banjara, "name": hyd_care_banjara["name"] + " (Diabetes)"},
    {**kol_apollo_gleneagles, "name": kol_apollo_gleneagles["name"] + " (Endocrinology)"}, {**kol_cmri, "name": kol_cmri["name"] + " (Endocrinology)"}, {**kol_peerless, "name": kol_peerless["name"] + " (Diabetes)"},
    {**nsk_apollo, "name": nsk_apollo["name"] + " (Endocrinology)"}, {**nsk_wockhardt, "name": nsk_wockhardt["name"] + " (Endocrinology)"},
    {**ahd_apollo, "name": ahd_apollo["name"] + " (Endocrinology)"},
    {**ngp_aiims, "name": ngp_aiims["name"] + " (Endocrinology)"}, {**ngp_kingsway, "name": ngp_kingsway["name"] + " (Diabetes)"}, # Nagpur Examples
    {**surat_kiran, "name": surat_kiran["name"] + " (Diabetes)"}, {**surat_sunshine, "name": surat_sunshine["name"] + " (Endocrinology)"}, # Surat Examples
    {**kanpur_regency, "name": kanpur_regency["name"] + " (Diabetes/Endocrinology)"},
    # Individual Doctors
     {"name": "Lifeline Hospital", "location": (16.7050, 74.2433), "rating": 4.8, "address":"Race Course Naka, Mangalwar Peth, Kolhapur", "contact": "9921341134"},
    {"name": "Dr. Khade's Center of neurology ", "location": (16.7050, 74.2433), "rating": 4.8, "address":"Mangalwar Peth, Kolhapur", "contact": "7721810077"},
    {"name": "Sahyadri Superspeciality Hospital Hadapsar", "location": (18.4995, 73.9212), "rating": 4.6, "address":"Bhosale Nagar, Hadapsar, Pune", "contact": "8888822222", "link": "https://sahyadrihospital.com/"},
    {"name": "Manipal Hospital Kharadi", "location": (18.5518, 73.9501), "rating": 4.5, "address":"Near Nyati Empire, Kharadi, Pune", "contact": "020 6165 6666", "link":"https://www.manipalhospitals.com/pune/"},
    {"name": "Jeevandhara Hospital", "location": (17.6805, 74.0183), "rating": 5.0, "address":"Kalyani Nagar, Satara", "contact": "7821992081"},
    {"name": "Kapre Neuro-Diagnostic Center", "location": (17.6805, 74.0183), "rating":4.7, "address":"Guruwar Peth, Satara", "contact": "2283174"},
    {"name": "Dr. Pradyumna Oak", "location": (19.0176, 72.8302), "rating": 4.3, "address": "Dadar west, Dadar, Mumbai", "contact": "24449161"},
    {"name": "Dr. Mohit Bhatt (Kokilaben Hospital)", "location": (19.1175, 72.8280), "rating": 3.8, "address": "Kokilaben Hospital, Andheri west, Mumbai", "contact": "42696969"},
    {"name": "Dr. Vishal Sawale", "location": (19.9975, 73.7898), "rating": 4.9, "address": "Neuro Plus Hospital, Ahilyadevi Holkar Road, Nashik", "contact": "7383560249"},
    {"name": "Dr. Ninad Thorat", "location": (19.9975, 73.7898), "rating": 4.8, "address": "Platina Hospital, Near Tup-Sakhare Lawns, Nashik", "contact": "9607799333"},
]

# ----------------------------------------------------------------------
# --- SANJEEVANI REMEDY DATA (<<< INTEGRATED USER DATA - VERIFY & REPLACE REMAINING PLACEHOLDERS) ---
# ----------------------------------------------------------------------
sanjeevani_data = {
    "Diabetes": {
        "Mild": {
            "Young": {
                 "Yoga": {
                    "Surya Namaskar (Sun Salutation)": { "steps": ["Sequence of 12 poses performed in a flow."], "duration": "5-10 rounds", "frequency": "Daily" },
                    "Trikonasana (Triangle Pose)": { "steps": ["Stand legs apart, arms sideways, bend to touch R foot with R hand, switch."], "duration": "Hold 30s each side", "frequency": "Daily" },
                    "Veerabhadrasana (Warrior Pose)": { "steps": ["Lunge forward with one leg, arms extended overhead."], "duration": "Hold 30s each side", "frequency": "Daily" }
                 },
                 "Pranayama": {
                    "Kapalbhati": {"steps": ["Sit meditative posture, straight spine.", "Hands knees Gyan Mudra, relax body.", "Normal inhale, exhale forcefully via nose, pull stomach inward.", "Inhalation passive.", "Continue rhythmically, focus exhalation."], "duration": "15 minutes", "frequency": "Once daily, AM empty stomach or 2hr post meal", "avoid": "Avoid if pregnant, during menstruation, or if you have hernia, high BP, recent abdominal surgery"},
                    "Anulom_Vilom": {"steps": ["Sit comfy, spine erect.", "Close R nostril (thumb).", "Inhale slow via L nostril.", "Close L nostril (ring finger), release R, exhale slow.", "Repeat other side for one cycle.", "Continue smooth, silent breathing."], "duration": "15 minutes", "frequency": "Min 1-2 times daily, anytime >30min post meal", "avoid": "Avoid during extreme congestion or agitation"},
                    "Bhramari": {"steps": ["Sit relaxed, eyes closed.", "Thumbs on ears, index fingers forehead, other fingers over eyes.", "Deep inhale via nose.", "Exhale slow, deep humming sound (mmm...), focus inward.", "Feel vibrations, remain calm."], "duration": "5-7 rounds (~5 mins)", "frequency": "1-2 times daily, esp. evening/stress", "avoid": "Avoid in loud surroundings or if prone to migraines/ear discomfort"}
                 },
                 "Naturopathy": {
                    "Morning Sunlight": {"steps": ["Expose face/limbs to early sunlight (7–8 AM)."],"duration": "20 minutes","frequency": "Daily"},
                    "Hydrotherapy": {"steps": ["Splash eyes with cool water", "Sit feet in warm water for calming nerves."], "duration": "5-10 mins", "frequency": "2 times daily"},
                    "Mud Pack": {"steps": ["Apply mud pack to abdomen (navel region).", "Lie down calmly until pack dries."], "duration": "20 minutes", "frequency": "Alternate days"},
                    "Foot Massage": {"steps": ["Massage feet with warm oil before bed."], "duration": "10 minutes", "frequency": "Daily"}
                 },
                 "Diet": {
                    "notes": "Emphasize low GI, fiber-rich foods with balanced nutrition. Avoid refined sugars and excess starches.",
                    "suggestions": ["Sprouted moong salad with lemon/cucumber", "Vegetable oats upma", "Methi thepla with curd", "Whole grain roti with lauki sabzi", "Brown rice with dal/steamed broccoli", "Vegetable dalia with flax seeds", "Bajra roti with baingan bharta", "Fruit bowl (apple, papaya, amla)", "Boiled chickpeas chat", "Besan chilla", "Idli with sambar (low salt/sugar)", "Salad before lunch"]
                 },
                 "Ayurveda": {
                    "notes": "Focus on pacifying Kapha and enhancing Agni. Avoid curd at night, excessive sweet & cold items.",
                    "herbs_decoctions": ["Amla juice (1 tbsp warm water, morning),Divya Madhunashini Vati 1 tablet twice a day , Divya Chandra Prabhavati 1 tablet twice a day, Giloy Ghanvati 2 twice a day or Giloy amla juice ", "Methi seed water (1 tsp soaked overnight)", "Neem leaves juice/capsule (consult dose)", "Triphala powder (bedtime, warm water)", "Jamun seed powder (1 tsp post lunch)"]
                 },
                 "ProTips": {
                    "notes": "Create consistent routine with activity, mindful eating, family wellness.",
                    "tips": ["Walk post meals (10-15 min).", "Break long sitting.", "Prefer homemade snacks.", "Sleep before 10 PM.", "Avoid screen 1hr before bed.", "Use cinnamon, turmeric.", "Prefer whole fruits over juices.", "Hydrate warm water.", "Morning yoga/breathing.", "Track fasting sugar weekly."]
                 }
            },
            "Adult": { # Using specific data you provided
                "Yoga": {
                    "Mandukasana (Frog Pose)": { "steps": [" Sit Vajrasana.", " Fists nr navel.", " Inhale, exhale bend forward, press.", "Hold.", "Inhale return."], "duration": "Hold 30s-1min", "frequency":"Daily AM/PM"},
                    "Vakrasana (Twisted Pose)": { "steps": ["Sit legs extended.", "Bend R leg, foot by L knee.", "R hand behind, L hand on R knee.", "Twist R.", "Hold, repeat L."], "duration": "Hold 10-15s/side", "frequency":"2-3 rounds daily"},
                    "Uttanapadasana (Raised Leg Pose)": { "steps": ["Lie back.", "Inhale, raise legs 45 deg.", "Hold.", "Exhale, lower."], "duration": "Hold 15-30s", "frequency":"3-5 rounds daily"},
                    "Pawanmuktasana (Wind-Relieving Pose)": { "steps": ["Lie back.", "Bend R knee to chest.", "Clasp, press.", "Lift head.", "Hold, switch."], "duration": "Hold 30s", "frequency":"2-3 times daily"},
                    "Naukasana (Boat Pose)": { "steps": ["Lie back.", "Inhale, lift legs, arms, upper body.", "Arms parallel.", "Hold, exhale return."], "duration": "Hold 15-30s", "frequency":"2-3 rounds daily"},
                    # Adding Asanas from Mild list as well for completeness
                    "Vrikshasana (Tree Pose)": { "steps": ["Stand feet together.", "Shift weight to L leg.", "Place R foot sole on inner L thigh or calf.", "Palms together at chest."], "duration": "30 seconds per side", "frequency": "Once daily" },
                    "Dhanurasana (Bow Pose)": { "steps": ["Lie on stomach, arms beside body.", "Bend knees, hold ankles.", "Inhale, lift chest & thighs.", "Hold briefly, lower."], "duration": "5–10 seconds", "frequency": "2–3 times daily" },
                    "Paschimottanasana (Seated Forward Bend)": { "steps": ["Sit legs extended straight.", "Inhale, lengthen spine.", "Exhale, hinge at hips, reach towards feet.", "Hold."], "duration": "20–30 seconds", "frequency": "Once daily" }
                },
                "Pranayama": { # Combined from multiple sections provided
                    "Kapalbhati": { "steps": ["Sit straight.", "Deep inhale.", "Forceful exhale via nose, contract abdomen.", "Passive inhale.", "Repeat rhythmically."], "duration": "Start 1-2 mins, build to 15 mins", "frequency": "Daily AM empty stomach", "avoid": "Pregnancy, menstruation, hernia, high BP, recent surgery"},
                    "Anulom Vilom": { "steps": ["Sit straight.", "Close R nostril (thumb), inhale L.", "Close L (ring finger), release R, exhale R.", "Inhale R, close R, exhale L.", "Continue pattern silently."], "duration": "15-30 mins total", "frequency": "1-2 times daily, anytime >30min post meal", "avoid": "Extreme congestion, agitation"},
                    "Bhastrika": { "steps": ["Sit straight.", "Inhale deep via nose.", "Exhale forcefully via nose.", "Repeat forcefully."], "duration": "2-3 mins (use caution!)", "frequency": "Daily AM empty stomach"},
                    "Bhramari": { "steps": ["Sit comfy, close eyes/ears.", "Inhale deep.", "Exhale humming 'mmmm', focus vibration."], "duration": "5-7 rounds (approx 5 mins)", "frequency": "1-2 times daily, esp. evening/stress", "avoid":"Loud places, migraines"},
                    "Udgith": {"steps": ["Chant 'Om' during slow exhalation."], "duration": "5-10 mins", "frequency": "Daily"},
                    "Ujjayi": {"steps": ["Slightly constrict throat, inhale/exhale via nose with soft sound."], "duration": "5-10 mins", "frequency": "Daily"}
                },
                "Diet": { # Using specific data provided
                    "breakfast": ["Sprouted fenugreek and moong dal (1 cup)", "Multigrain porridge (1 bowl)"],
                    "lunch": ["Multigrain roti (2 pieces) with mixed vegetables (1 cup)"],
                    "dinner": ["Light vegetable soup (1 bowl)", "Cucumber, bitter gourd, and tomato juice (1 glass)"],
                    "regional_recipes": ["Besan Cheela (minimal oil)", "Ragi Mudde", "Thepla (methi, minimal oil)", "Veg Poha", "Dalma"],
                     "good_vegetables": {"general": ["Bitter gourd (1/2 cup daily)", "Cucumber (1/2 cup daily)", "Tomato (1 medium daily)", "Leafy Greens", "Gourds", "Beans", "Okra"], "breakfast_lunch": ["Variety"], "dinner": ["Cooked focus"]},
                     "good_fruits": ["Amla (1-2 fruits per day)", "Jamun", "Guava"],
                     "weekly_fasting_suggestion": "**Consult Doctor/Dietitian FIRST.** If approved, consider fruit-only or liquid-only day. NO unsupervised fasting.",
                     "emphasize": ["High-fiber foods", "Low glycemic index foods", "Bitter Gourd", "Methi", "Turmeric", "Cinnamon"],
                     "avoid": ["Sugary fruits (excess)", "Processed foods", "Sugar", "Maida", "White Rice", "Fried foods", "High-calorie foods", "Unhealthy snacks"],
                     "timing_notes": "Maintain regular meal timings. Avoid late-night eating. Avoid long periods without meals."
                 },
                 "Naturopathy": { # Using specific data provided
                    "Morning Walk": {"steps": ["Walk briskly"], "duration": "30-45 minutes", "frequency": "Early morning, empty stomach"},
                    "Sunbathing": {"steps": ["Sit in direct sunlight"], "duration": "10-15 minutes", "frequency": "Morning (7-9 AM)"},
                    "Medicated Water - Methi": {"steps": ["Soak 1 tsp methi seeds overnight.", "Drink water next morning."], "frequency": "Daily"},
                    "Medicated Water - Cinnamon": {"steps": ["Boil cinnamon stick in water.", "Drink when cool."], "frequency": "Occasionally"},
                    "Medicated Water - Tulsi": {"steps": ["Boil 6-8 tulsi leaves in water.", "Drink when cool."], "frequency": "Occasionally"}
                 },
                 "Ayurveda": { # Using specific data provided
                    "lifestyle_principles": ["Maintain Routine (Dinacharya)", "Balanced diet", "Manage Agni"],
                    "herbs_decoctions": ["Divya Madhunashini Vati (2 tablets twice a day)", "Divya Chandraprabha Vati", "Karela Juice (1 glass morning/evening)", "Giloy Ghanvati Advance", "Amla Juice (1 tbsp daily)", "Vijaysar Powder", "Methi Powder (1 tsp morning)", "Divya Shilajeet Rasayan Vati", "Triphala Churna", "Neem Ghanvati"],
                    "notes": "Dosage and suitability require individual assessment by a practitioner."
                 },
                "ProTips": {
                    "lifestyle": ["Regular BG monitoring!", "Foot care!", "No smoking/alcohol.", "Regular check-ups.", "Consider Karela/Jamun seed powder."]
                 }
            },
            "Senior": { # Using specific data provided
                "Yoga": {
                    "asanas": [ "Chair-supported Tadasana", "Seated Ardha Matsyendrasana", "Supta Baddha Konasana (Reclining Bound Angle Pose)", "Seated Cat-Cow Stretch", "Leg Lifts (seated)", "Viparita Karani (Legs-up-the-wall, supported)", "Shavasana (Relaxation Pose)" ],
                    "steps_note": "All poses slow, with support. Avoid forward bends/intense balance.",
                    "duration": "20-30 mins", "frequency": "Daily AM or PM",
                    "notes": "Use cushions/chairs. Consult therapist. Breathe gently via nose."
                 },
                "Pranayama": {
                    "Anulom Vilom": { "steps": ["Sit upright.", "Close R nostril, inhale L.", "Close L, exhale R.", "Repeat reverse.", "Slowly without strain."], "duration": "15-30 mins total", "frequency": "Daily, >30min post meal or empty" },
                    "Bhramari": { "steps": ["Sit comfy, eyes closed.", "Close ears, inhale deep.", "Exhale humming.", "Repeat 5-7 rounds."], "duration": "5-10 mins", "frequency": "Daily AM or PM" },
                    "Chandra Bhedana": { "steps": ["Close R nostril, inhale L.", "Close L, exhale R.", "Repeat gently, cooling breath."], "duration": "5 mins", "frequency": "As needed for calm" }
                 },
                 "Naturopathy": {
                     "practices": ["Warm water foot soak (10m before sleep)", "Morning sun (10–15m pre-9 AM)", "Oil massage (weekly, warm sesame)", "Gentle walk post meals (5-10m)"],
                     "medicated_water": ["Soaked methi seeds (1 tsp overnight, chew morning)"],
                     "notes": "Keep warm. Avoid cold compresses."
                 },
                 "Diet": {
                    "breakfast": ["Steamed oats w/ cinnamon", "Soft moong dal chilla", "Veg upma", "Soft poha", "Ragi porridge", "Idli w/ sambar", "Boiled sweet potato", "Fruit bowl (apple, papaya, guava)", "Herbal tea", "Cucumber/tomato slices"],
                    "lunch": ["Soft chapati (1-2), methi sabzi", "Khichdi w/ bottle gourd", "Lauki-tomato curry + rice (small)", "Dal + steamed veg + salad"],
                    "dinner": ["Moong dal soup", "Light kichadi", "Oats/barley porridge (salted)", "Veg stew w/ soft roti"],
                    "emphasize": ["Warm, fresh cooked food", "Low glycemic, fibrous", "Hydration (warm water)", "Early dinner (<7 PM)"],
                    "avoid": ["Cold items (curd night)", "Excess Sugar/jaggery/sweet fruits", "Spicy/oily food", "Processed snacks"]
                 },
                 "Ayurveda": {
                     "herbs_decoctions": ["Triphala decoction (bedtime)", "Gudmar (consult)", "Neem capsule, Divya Madhunashini Vati, Giloy Ghanvati(consult)", "Fenugreek powder"],
                     "notes": "Avoid overuse. Consult for dosage. Emphasize digestion."
                 },
                 "ProTips": {
                     "lifestyle": ["Keep footwear nearby", "Hydrate warm", "Daily seated stretch", "Avoid post-meal naps", "Monitor sugar weekly", "Family involvement"],
                     "emotional_wellbeing": ["Gratitude journal", "Spiritual reading/bhajans", "Nature walks", "Consistent sleep"]
                 }
            }
        },
        "Moderate": { # Populated with descriptive notes provided by user
            "Young": {"notes": "Moderate Diabetes (Young): Emphasize early lifestyle correction. Balanced, low-sugar, high-fiber diet. Active outdoor games/yoga (Surya Namaskar, Tadasana). Pranayama (Anulom Vilom, Bhramari). Mindfulness, digital detox, family support. Build lifelong habits."},
            "Adult": {"notes": "Moderate Diabetes (Adult): Combine conventional treatment & lifestyle. Regular meds, HbA1c monitoring, tailored nutrition (portion control, low-GI). Moderate yoga (Trikonasana, Vajrasana, Setu Bandhasana). Daily Pranayama (Kapalbhati, Nadi Shodhana). Psychological support. Ayurveda explored with clinical oversight."},
            "Senior": {"notes": "Moderate Diabetes (Senior): Holistic geriatric care: meds adherence, gentle diet, frequent complication checks. Mild yoga (Chair Yoga, Shavasana, supported Balasana). Calming Pranayama (Anulom Vilom, Ujjayi). Involve caregivers, emotional support, spiritual spaces. Focus on dignity, independence."}
        },
        "Severe": { # Populated with descriptive notes provided by user
            "Young": {"notes": "Severe Diabetes (Young): Full-spectrum care: insulin therapy, stress management, resilience building. Blend modern medicine with regulated yoga (Ardha Matsyendrasana, Dhanurasana) & Pranayama (Kapalbhati, Bhramari). Creative therapies, digital support, counseling. Peer/family support."},
            "Adult": {"notes": "Severe Diabetes (Adult): Layered care: medical treatment, complication monitoring (feet, eyes, kidneys). Structured Yoga (Paschimottanasana, Bhujangasana) & Pranayama (Kapalbhati, Ujjayi). Weekly mindfulness, stress reduction rituals. Low-impact aerobics. Guided meditation & positive spiritual practices."},
            "Senior": {"notes": "Severe Diabetes (Senior): Empathy key: manage insulin/meds safely, monitor vitals, comfort nutrition. Restorative yoga (Shavasana, gentle leg lifts), seated Pranayama (Anulom Vilom, Bhramari). Spiritual bonding (mantras, stories). Support dignity, light exercise, safe companionship."}
        }
    },
    "Heart Disease": {
        "Mild": {
            "Young": { # Populated with user input notes
                 "Yoga": {"notes": "Focus on prevention/stress relief. Include Surya Namaskar, Tadasana, Bhujangasana to enhance cardiovascular fitness."},
                 "Pranayama": {"notes": "Practice Anulom Vilom, Bhramari, Nadi Shodhana daily for stress reduction."},
                 "Diet": {"notes": "Heart-friendly diet: leafy greens, berries, nuts, omega-3s (flaxseeds). Avoid deep-fried/processed."},
                 "Naturopathy": {"notes": "Encourage warm water hydration, sun exposure (15 mins), tulsi-ginger water."},
                 "Ayurveda": {"notes": "Arjuna bark tea/powder under supervision; Triphala for digestion."},
                 "ProTips": {"notes": "Limit screen time, cultivate hobby, schedule annual checkups."}
             },
            "Adult": { # Integrated provided data
                "Yoga": {
                    "Tadasana (Mountain Pose)": {"steps": ["Stand tall, stretch arms up."], "duration": "Hold 1 min", "frequency": "5 rounds daily"},
                    "Setu Bandhasana (Bridge Pose)": {"steps": ["Lie back, knees bent, lift hips."], "duration": "Hold 30s", "frequency": "3-5 rounds daily"},
                    "Utkatasana (Chair Pose)": {"steps": ["Stand, bend knees as if sitting, arms up."], "duration": "Hold 20-30s", "frequency": "Once daily"},
                    "Ardha Matsyendrasana": {"steps": ["Sit, bend R knee over L, twist R."], "duration": "30s/side", "frequency": "3-5 rounds daily"},
                    "Bhujangasana (Cobra Pose)": {"steps": ["Lie face down, lift chest."], "duration": "15-30s", "frequency": "2-3 rounds daily"}
                 },
                 "Pranayama": {
                    "Ujjayi (Victorious Breath)": {"steps": ["Sit comfy, constrict throat slightly, breathe via nose with sound."], "duration": "5-10 mins", "frequency": "1-2 times daily"},
                    "Bhastrika (Bellows Breath)": {"steps": ["Sit comfy, inhale deep, exhale force via nose. Repeat."], "duration": "1-2 mins", "frequency": "Once daily (Caution!)"}
                 },
                 "Naturopathy": {
                     "Hydrotherapy (Contrast Compress)": {"steps": ["Alternate hot (3-5m) & cold (1m) on chest."], "frequency": "Once daily (Consult)"},
                     "Morning Walk": {"steps": ["Brisk walk"], "duration":"30 mins", "frequency":"Daily"},
                     "Sunbathing": {"steps": ["Expose face/arms"], "duration":"10 mins", "frequency":"Early AM/PM"},
                     "Dietary Adjustments": {"recommendations": ["Increase fruits/veg.", "Limit sat fats/cholesterol.", "Whole grains/legumes."]}
                 },
                 "Diet": {
                     "breakfast": ["Oats porridge w/ chia/berries", "Warm lemon water"], "lunch": ["Brown rice w/ lentils/veg", "Veg juice"], "dinner": ["Light soup", "Salad w/ olive oil"],
                     "good_vegetables": {"general": ["Spinach", "Tomatoes", "Carrots"]}, "good_fruits": ["Papaya", "Apple", "Banana"],
                     "emphasize": ["Omega-3s", "Whole grains", "Lean proteins", "Low sodium"], "avoid": ["Trans/Sat fats", "Sugar", "Processed meats", "Excess salt"], "timing_notes": "Regular timings."
                 },
                 "Ayurveda": {
                     "herbs_decoctions": ["Arjunarishta (2 tbsp twice daily )", "Ashwagandha (1-2 g daily )", "Tulsi Ginger Tea", "Divya Hridyamrit Vati", "Divya Mukta Vati", "Divya Sarvkalp Kwath", "Giloy Ghanvati Advance", "Amla Juice", "Divya Medohar Vati", "Divya Panchamrit Parpati", "Divya Yogendra Ras"],
                     "notes": "Coordinate ALL herbs with Cardiologist/Practictioner at any patanjali megastore or refer Divya Pharmacy Containers ."
                 },
                 "ProTips": {
                     "lifestyle": ["Green leafy veg.", "Turmeric/ginger.", "Avoid fried.", "Healthy fats.", "Monitor cholesterol/BP."]
                 }
            },
            "Senior": { # Populated with user input notes
                 "Yoga": {"notes": "Gentle, consistent efforts. Practice simple poses: Chair Yoga, Shavasana, Setu Bandhasana (supported). Increase blood flow without strain."},
                 "Pranayama": {"notes": "Anulom Vilom, Ujjayi, Bhramari - soothing and safe."},
                 "Diet": {"notes": "Focus on easily digestible khichdi, boiled vegetables, fruits (papaya, apple); avoid excess salt/oil."},
                 "Naturopathy": {"notes": "Foot soaks, light oil massages, early morning sunbathing."},
                 "Ayurveda": {"notes": "Arjuna, Ashwagandha (emotional balance), Dashamoola under supervision."},
                 "ProTips": {"notes": "Keep emergency contact visible, medication reminders, engage in satsangs/storytelling."}
            }
        },
        "Moderate": { # Populated with user input notes
            "Young": {"notes": "Proactive, guided changes. Yoga (Trikonasana, Matsyasana, Pawanmuktasana). Pranayama (Kapalbhati-moderate, Bhramari, Nadi Shodhana). Low-sodium/fat diet (millets, lentils, soups). Amla/turmeric moderation. Naturopathy (Steam inhalation, grounding walks). Ayurveda (Arjuna+honey, Brahmi). Monitor BP."},
            "Adult": {"notes": "Structured approach: medication + holistic. Yoga (Warrior Pose, Viparita Karani, gentle twists). Pranayama (Nadi Shodhana, Bhramari, light Ujjayi). Heart-smart meals (oats, turmeric milk, methi, berries, seeds). Naturopathy (Hot foot baths, lemon-honey water). Ayurveda (Arjuna, Pushkarmool, Yashtimadhu supervised). Gratitude journal, 7hrs sleep."},
            "Senior": {"notes": "Calming, restorative care. Gentle yoga (Sukhasana, supported Ardha Matsyendrasana). Pranayama (Anulom Vilom, Bhramari, soft deep breathing). Diet (Seasonal soups, moong dal, pumpkin, beetroot). Reduce salt, avoid fried. Naturopathy (Foot reflexology, neem bath). Ayurveda (Arjuna, Guggulu - expert approval!). Companionship, prayer spaces."}
        },
        "Severe": { # Populated with user input notes
            "Young": {"notes": "Integrate medical treatment + holistic aids. Gentle restorative yoga (Balasana, supported Setu Bandhasana, Viparita Karani - expert supervision!). Pranayama (Deep Ujjayi, Bhramari, guided visualization). Personalized low-sodium diet. Avoid stimulants. Naturopathy (Sun exposure, hydration, Epsom salt foot soaks). Ayurveda (Hridaya herbs: Arjuna, Giloy - medical advice!). Stay positive."},
            "Adult": {"notes": "Doctor-guided changes, gradual holistic reinforcement. Limited yoga (stretches, supported Supta Baddha Konasana). Pranayama (Soft Bhramari, abdominal breathing). Controlled salt diet, herbal teas (hibiscus, tulsi). Avoid stimulants (coffee/tea). Naturopathy (Warm compresses, oil rubs, stress detox). Ayurveda (Arjuna+honey, Brahmi ghrita). Calm routines."},
            "Senior": {"notes": "Elderly severe heart issues require utmost care. Yoga (Passive movements, guided visual meditations, minimal Chair Yoga). Pranayama (Anulom Vilom gentle, Om chanting, silent breath observation). Diet (Khichdi, soft fruits, cardamom milk). Naturopathy (Foot soaks, warm herbal compresses, sun). Ayurveda (Arjuna, Dashamoola, Ashwagandha - physician oversight!). Simplify routines, emotional check-ins, calming music."}
        }
    },
     "Parkinsons": {
        "Mild": {
            "Young": { # Populated with user input notes
                "Yoga": {"notes": "Manage early onset with brain-supportive routines. Practice Vrikshasana, Trikonasana, Utkatasana for balance/posture."},
                "Pranayama": {"notes": "Nadi Shodhana, Bhramari, Ujjayi improve neural oxygenation, reduce stress."},
                "Diet": {"notes": "Include omega-3s, leafy greens, cow milk, turmeric. Avoid refined sugar/stimulants."},
                "Naturopathy": {"notes": "Steam baths, sunrise walks barefoot, warm neem water hand-soaks."},
                "Ayurveda": {"notes": "Use Brahmi, Ashwagandha, Shankhpushpi supervised; cow ghee for neural lubrication."},
                "ProTips": {"notes": "Hand-eye coordination exercises, digital detox, journaling."}
            },
            "Adult": { # Populated with specific user data
                 "Yoga": {
                     "Trikonasana (Triangle Pose)": {"steps": ["Legs apart, extend arms, tilt side, hand on shin, gaze up."], "duration": "Hold 30s/side", "frequency": "3-5 rounds daily"},
                     "Virabhadrasana I (Warrior I Pose)": {"steps": ["Step forward, bend knee, arms overhead."], "duration": "Hold 30s/side", "frequency": "2-3 rounds daily"},
                     "Supta Baddha Konasana (Reclining Bound Angle)": {"steps": ["Lie back, soles together, knees drop wide."], "duration": "Hold 1-2 mins", "frequency": "3-5 rounds daily"},
                     "Seated Cat-Cow Stretch": {"steps": ["Sit chair. Inhale arch, Exhale round."], "duration": "1-2 mins", "frequency": "2-3 times daily"},
                     "Chair Warrior II": {"steps": ["Sit, arms parallel, turn head."], "duration": "20-30s/side", "frequency": "Once daily"},
                     "Seated Leg Extensions": {"steps": ["Sit chair, extend R leg, hold, lower. Repeat L."], "duration": "1 min/leg", "frequency": "2-3 times daily"}
                 },
                 "Pranayama": {
                     "Bhramari (Humming Bee Breath)": {"steps": ["Sit comfy, close eyes/ears, hum exhale."], "duration": "5-10 rounds", "frequency": "2-3 times daily"},
                     "Nadi Shodhana (Alternate Nostril)": { "steps": ["Sit comfy, use thumb/finger alternate nostrils."], "duration": "5–10 minutes", "frequency": "1-2 times daily" }
                 },
                 "Naturopathy": {
                     "Foot Massage": {"steps": ["Warm sesame/coconut oil, massage feet."], "duration":"5-10 mins/foot", "frequency": "Daily before bed"},
                     "Gentle Walks": {"steps": ["Comfy pace, steady breathing."], "duration": "10–15 minutes", "frequency": "2–3 times daily"},
                 },
                 "Diet": {
                     "breakfast": ["Oats w/ walnuts/flaxseeds", "Warm ginger lemon water"], "lunch": ["Quinoa w/ sautéed veg", "Carrot/cucumber salad"], "dinner": ["Lentil soup w/ spinach", "Avocado toast"],
                     "good_vegetables": {"general": ["Leafy greens", "Carrots", "Beetroot"]}, "good_fruits": ["Banana", "Papaya", "Blueberries"],
                     "emphasize": ["Omega-3s", "High-fiber", "Hydration"], "avoid": ["Heavy/greasy", "Processed", "Protein timing issues w/ Levodopa (Consult!)"],
                     "timing_notes": "Stay hydrated."
                 },
                 "Ayurveda": {
                     "herbs_decoctions": ["Divya Medha Vati (1 tab twice daily)", "Ashwagandha (1-2g daily)", "Ekangveer Ras", "Brahmi Vati", "Shilajeet Rasayan Vati", "Swarn Makshik Bhasma", "Rasraj Ras", "Mucuna Pruriens (Kapikachhu) (1 tsp morning - **STRICTLY CONSULT NEUROLOGIST**)", "Yogendra Ras", "Giloy Ghanvati Advance"],
                     "lifestyle_principles": ["Vata balancing", "Regular routine", "Abhyanga"], "notes": "Coordinate Kapikachhu w/ Dr."
                 },
                 "ProTips": {
                     "lifestyle": ["Stretching/walking.", "Speech exercises.", "Meditation.", "Hydration.", "Bowel regularity.", "Consider Ashwagandha, Mucuna Pruriens, Turmeric."]
                 }
            },
            "Senior": { # Populated with user input notes
                 "Yoga": {"notes": "Improve mobility & emotional balance. Chair Yoga, Tadasana, supported Setu Bandhasana with caregiver."},
                 "Pranayama": {"notes": "Bhramari, Anulom Vilom, deep abdominal breathing for calmness."},
                 "Diet": {"notes": "Warm khichdi, soft-cooked veg, figs, cow milk+turmeric. Avoid dry/spicy."},
                 "Naturopathy": {"notes": "Foot massages (warm sesame oil), lukewarm lemon water detox, nasal oiling supervised."},
                 "Ayurveda": {"notes": "Brahmi ghrita, Dashamoola for stiffness, Vata-pacifying diet."},
                 "ProTips": {"notes": "Involve in bhajans/spiritual sessions, use large-handle utensils, label items."}
            }
        },
        "Moderate": {
            "Young": {"notes": "Moderate Parkinson's (Young): Structure routines for motor coordination & clarity. Yoga (Vrikshasana-wall, supported Virabhadrasana, Cat-Cow). Pranayama (Bhramari, Nadi Shodhana, soft Kapalbhati guided). Diet (Warm meals, antioxidants: spinach, coconut water, soaked almonds). Avoid cold/raw. Naturopathy (Warm castor oil massage, sunbathing). Ayurveda (Brahmi, Shankhpushpi syrups, Ashwagandharishta). Cues, sleep schedule."},
            "Adult": { # Populated with specific user data
                 "Yoga": {
                     "Vrikshasana (Tree Pose)": {"steps": ["Stand straight, foot on opp. thigh.", "Palms Namaste overhead.", "Focus, hold 30s.", "Switch."], "duration":"30s/side", "frequency":"Daily"},
                     "Trikonasana (Triangle Pose)": {"steps": ["Legs wide, arms shoulder level.", "Bend side, touch ankle, gaze up.", "Hold.", "Switch."], "duration":"20-30s/side", "frequency":"Daily"},
                     "Vajrasana with Forward Bend": {"steps": ["Sit Vajrasana, bend forward, forehead floor.", "Arms forward/alongside."], "duration":"Hold 30s", "frequency":"Daily"}
                 },
                 "Pranayama": {
                     "Anulom Vilom": {"steps": ["Alternate nostril breathing."],"duration":"5-10 mins", "frequency":"Daily"},
                     "Bhramari": {"steps": ["Humming bee breath."], "duration":"5-10 mins", "frequency":"Daily"},
                     "Ujjayi": {"steps": ["Throat constriction breath."], "duration":"5 mins", "frequency":"Daily"}
                 },
                 "Naturopathy": { "medicated_water": ["Brahmi water (1 tsp boiled)."] },
                 "Diet": {"notes": "Manage non-motor symptoms (constipation, swallowing). Nutrient density important. Protein timing needs care."},
                 "Ayurveda": {"notes": " Divya Medha Vati Extra Power to calm the nervous system and support brain function; it is generally taken as one to two tablets twice daily after meals with water or milk. Divya Ekangveer Ras for neurological issues and may be taken at a dose of 125 mg twice daily with honey or warm water. Another potent classical formulation, Divya Brihat Vata Chintamani Ras, is often suggested in cases of vata imbalance affecting the nervous system, with a dose of 125 mg once or twice a day with honey, but only under medical supervision due to its metallic content.Divya Makar Dhwaj Ras, known for enhancing vitality and physical coordination, is also used cautiously under expert guidance. Divya Vat Vidhvansan Ras is considered helpful in reducing tremors and is typically taken as one tablet twice daily with warm water. In addition, Ashwagandha in capsule or powder form is advised to strengthen the nervous system and relieve stress; usually, one capsule is taken twice a day or one teaspoon of powder with warm milk at bedtime. To support overall energy and rejuvenation, Divya Shilajeet Rasayan Vati is commonly used, taken as one tablet twice daily with warm water or milk .Consult Vaidya for moderate stage support. May need stronger Vata balancing."},
                 "ProTips": {"lifestyle": ["Physical/Occupational therapy integration vital.", "Regular exercise crucial."]}
            },
            "Senior": { "notes":"Moderate Parkinson's (Senior): Supportive care, emotional balance, motor function priority. Yoga (Sukhasana-supported, modified Trikonasana-chair, hand stretches). Pranayama (Nadi Shodhana, Bhramari, Om chanting). Diet (Ragi porridge, moong dal, banana, rice+ghee). Avoid hard foods. Naturopathy (Herbal warm compress, neem-turmeric paste). Ayurveda (Dashamoola kwath, Brahmi ghee, Anu taila supervised). Memory games, social support." }
        },
        "Severe": {
             "Young": {"notes":"Severe Parkinson's (Young): Calm, guided lifestyle. Mind-body focus. Yoga (Passive assisted stretches, restorative Supta Baddha Konasana-props). Pranayama (Deep Ujjayi, Bhramari supervised). Diet (Easy digest+ghee, barley soup, soft methi paratha). Avoid stimulants. Naturopathy (Steam face, turmeric foot soaks,team Inhalation for Face & Head: Add tulsi or mint leaves in water to calm nerves and improve circulation.Turmeric Foot Soaks: Warm water with turmeric and Epsom salt—daily soak for 10–15 minutes to relieve stiffness and enhance grounding.Sunlight therapy: Morning sun (before 9 AM) for 15 minutes to absorb Vitamin D and boost mood.). Ayurveda (Ashwagandha + Brahmi Capsules: Strengthen the nervous system, support calmness and memory. Take with warm milk.Chyawanprash (Rasayana): 1 tsp daily in the morning for rejuvenation and immunity. Abhyanga (Oil Massage): Full-body massage with Bala Taila or Mahanarayan Taila, followed by warm water bath. Reduces rigidity, calms tremors. Consider Shirodhara or Panchakarma (only at certified Ayurvedic centers and with supervision).). Simplify environment, sound cues, music therapy." },
             "Adult": {"notes":"Severe Parkinson's (Adult): Balance physical assist & neuro-support. Yoga (eated Neck & Shoulder Rolls (Chair or Floor) - ✅ Improves flexibility, reduces stiffness - Sit upright on a chair or floor with back support. Slowly roll your shoulders backward in circular motion – 5 rounds. Now forward – 5 rounds. Then gently tilt the  -head: up-down, side-to-side, ear-to-shoulder – 5 reps each. 🧘 Support head/shoulders with hand if needed. Hand Mobility Yoga - ✅ Boosts circulation & coordination - Open and close fists slowly – 10 times. Finger walking: walk fingers on a table up and down. Wrist rotations clockwise/anti-clockwise – 10 times. Finger stretching: stretch each finger gently. Seated Forward Bend (Paschimottanasana – Chair Version) ✅ Calms mind, stretches spine - Sit on chair, feet flat. Inhale, raise hands. Exhale, slowly bend forward with hands sliding toward feet. Stay for a few breaths, return slowly. Use cushion or block to support belly/chest). Pranayama (Anulom Vilom, soft deep abdominal). Diet (Moong dal soup, turmeric milk, soaked raisins, amla chutney). Avoid sour/cold. Naturopathy (Lukewarm sponge baths – Gentle cleansing, refreshes body, boosts circulation. Digestive teas – Cumin-fennel tea, ajwain water, or mint-ginger tea after meals. Warm foot soak – Optional: Epsom salt + turmeric 10 mins at night.). Ayurveda (Brahmi 1 tablet  – For memory & stress relief. Guduchi (Giloy) 2 tablets a day– Immunity & inflammation support. 1  tablet of Arjunavati – Heart-strengthening herb. All herbs to be taken in capsule or decoction form under Ayurveda practitioner guidance. Medicated head oil massage (Shiro Abhyanga) – Use oils like Brahmi Taila or Ksheerabala Taila. Massage scalp gently in circular motions 10–15 mins before bath.). Structured routines, art therapy, oral hygiene.tructured Routines – Fixed waking, meal, activity, and sleep times. Art & Music Therapy – Drawing, coloring, listening to devotional/classical music daily. Oral Hygiene – Tongue cleaning, herbal mouth rinse (triphala, clove oil-based), regular brushing." },
             "Senior": { # Populated with specific user data
                 "Yoga": {
                    "Chair Tadasana": {"steps": ["Sit chair, raise arms inhale, stretch spine, release exhale."], "duration":"Hold 15-20s", "frequency":"Several times daily"},
                    "Chair Twist": {"steps": ["Sit chair, R hand on L thigh, twist gently L. Hold. Repeat."], "duration":"Hold 15s/side", "frequency":"Daily"},
                    "Shavasana (Corpse Pose)": {"steps": ["Lie down, relax consciously."], "duration":"5-10 mins", "frequency":"Daily"}
                 },
                 "Pranayama": {
                     "Bhramari": {"steps": ["Softly forced exhalation."], "duration":"5 mins", "frequency":"Daily"},
                     "Chandra Bhedan (Left Nostril Breathing)": {"steps": ["Close R nostril, inhale L, Exhale R. Repeat."], "duration":"5 mins", "frequency":"Daily (calming)"}
                 },
                 "Naturopathy": {
                     "practices": ["Assisted gentle exercise", "Passive range of motion", "Emotional support"],
                     "medicated_water": ["Almond(5)/Walnut(2)/Brahmi(1tsp) blend soaked overnight, blended morning."]
                 },
                 "Diet": {"notes": "Focus on easy swallow, nutrient dense, prevent weight loss. Manage constipation. Soft foods, high fiber."},
                 "Ayurveda": {"notes": "Supportive care, coordinate with Neurologist. Focus on comfort.eated Neck & Shoulder Rolls (Chair or Floor) - For severe Parkinson’s in elderly individuals, Patanjali recommends a combination of Divya Medha Vati Extra Power for mental clarity, Ekangveer Ras and Rasraj Ras for nerve support, Swarn Makshik Bhasma, Praval Pishti, and Giloy Sat for vitality, Makar Dhwaj Ras for rejuvenation, Trayodashang Guggulu for joint health, Chandraprabha Vati for detox, and Shilajit Sat for stamina. These are to be taken under supervision, with tablets typically consumed twice daily.."},
                 "ProTips": {"lifestyle": ["Simplify environment.", "Caregiver support vital.", "Fall prevention crucial.", "Avoid muscle strain."]}
            }
        }
    }
}
# --- END OF SANJEEVANI DATA ---

# ----------------------------------------------------------------------
# --- FUNCTION TO DISPLAY SANJEEVANI ADVICE (Updated Formatting) ---
# ----------------------------------------------------------------------
def display_sanjeevani_advice(disease, age_str, severity_str):
    """Retrieves and displays holistic advice based on disease, severity, and age."""
    st.markdown("---"); st.markdown(f"<div class='sanjeevani-section'>", unsafe_allow_html=True)
    st.subheader("🌿 Sanjeevani Holistic Remedy Companion")
    st.caption("_Note: Guidance is illustrative & based on general principles/user input. Severity is subjective. Consult qualified professionals._")

    # Determine age group logic...
    age_group = "Adult"; user_age = None
    if age_str is not None and age_str.isdigit():
        try:
            user_age = int(age_str)
            if user_age < 18: age_group = "Young"
            elif user_age >= 60: age_group = "Senior"
        except ValueError: st.warning("Could not parse age; using Adult age group for advice.")
    else: st.warning("Age input missing/invalid; using Adult age group for advice.")
    # Determine severity logic...
    valid_severities = ["Mild", "Moderate", "Severe"]; severity = severity_str.strip().capitalize()
    if severity not in valid_severities: severity = "Moderate"; st.warning(f"Invalid severity; defaulting to Moderate.")
    # Prioritized Lookup Logic...
    lookup_order = [(severity, age_group), (severity, "Adult")]
    if severity == "Severe": lookup_order.extend([("Moderate", age_group), ("Moderate", "Adult"),("Mild", age_group), ("Mild", "Adult")])
    elif severity == "Moderate": lookup_order.extend([("Mild", age_group), ("Mild", "Adult")])
    advice = None; found_level = None; disease_data = sanjeevani_data.get(disease, {})
    for sev, age_g in lookup_order:
        temp_advice = disease_data.get(sev, {}).get(age_g)
        # Check if advice has substantial content (more than just a notes key perhaps)
        if temp_advice and any(k != "notes" and isinstance(temp_advice[k], (dict, list)) and temp_advice[k] for k in temp_advice):
             advice = temp_advice; found_level = f"{sev} / {age_g}"; break
        elif temp_advice and not advice: # Keep first found advice even if minimal
             advice = temp_advice; found_level = f"{sev} / {age_g}"

    # --- Display Section ---
    if advice:
        original_request = f"{severity} / {age_group}";
        if found_level and found_level != original_request: st.caption(f"_Showing guidance for {found_level} as specific advice for {original_request} wasn't available._")

        # --- Display Yoga ---
        yoga_info = advice.get("Yoga", {});
        if yoga_info and isinstance(yoga_info, dict):
             if any(k not in ["notes", "frequency", "steps_note"] for k in yoga_info): # Check if there's more than notes
                 with st.expander("🧘 Yoga Asanas", expanded=False):
                    asana_count = 0
                    for asana_name, details in yoga_info.items():
                         if asana_name not in ["pranayama", "frequency", "notes", "how_to_do", "steps_note"]:
                             st.markdown(f"**{asana_name}**")
                             if isinstance(details, dict) and details.get("steps"):
                                 st.markdown("**How:**\n" + "\n".join([f"  {i+1}. {s.strip()}" for i, s in enumerate(details["steps"])]))
                                 if details.get("duration"): st.markdown(f"  **Duration:** {details['duration']}")
                                 if details.get("frequency"): st.markdown(f"  **Frequency:** {details['frequency']}")
                                 st.markdown("---")
                             asana_count += 1
                    if yoga_info.get("steps_note"): st.markdown(f"**Asana Notes:** {yoga_info['steps_note']}")
                    if yoga_info.get("notes") and not yoga_info.get("steps_note"): st.markdown(f"**Notes:** {yoga_info['notes']}")
                    if yoga_info.get("frequency") and asana_count > 0 : st.markdown(f"**Overall Frequency:** {yoga_info['frequency']}")
             elif yoga_info.get("notes"): # Only display notes if ONLY notes exist
                 with st.expander("🧘 Yoga Asanas", expanded=False):
                     st.markdown(f"{yoga_info['notes']}")


        # --- Display Pranayama ---
        pranayama_info = advice.get("Pranayama", {});
        if pranayama_info and isinstance(pranayama_info, dict):
             if any(k != "notes" for k in pranayama_info):
                with st.expander("🌬️ Pranayama (Breathing Exercises)"):
                    for pranayama_name, details in pranayama_info.items():
                         if pranayama_name != "notes":
                             st.markdown(f"**{pranayama_name}**")
                             if isinstance(details, dict) and details.get("steps"):
                                 st.markdown("**How:**\n" + "\n".join([f"  {i+1}. {s.strip()}" for i, s in enumerate(details["steps"])]))
                                 if details.get("duration"): st.markdown(f"  **Duration:** {details['duration']}")
                                 if details.get("frequency"): st.markdown(f"  **Frequency:** {details['frequency']}")
                                 if details.get("avoid"): st.markdown(f"  **Avoid If:** {details['avoid']}")
                                 st.markdown("---")
                             elif isinstance(details, list): st.markdown(", ".join(details)) # Fallback
                    if pranayama_info.get("notes"): st.markdown(f"**Notes:** {pranayama_info['notes']}")
             elif pranayama_info.get("notes"): # Only display notes if ONLY notes exist
                  with st.expander("🌬️ Pranayama (Breathing Exercises)"):
                     st.markdown(f"{pranayama_info['notes']}")


        # --- Display Diet ---
        diet_info = advice.get("Diet", {});
        if diet_info and isinstance(diet_info, dict):
             if any(k != "notes" for k in diet_info):
                 with st.expander("🍎 Dietary Guidelines"):
                     # ... (Display diet details - same as before) ...
                     if diet_info.get("breakfast"): st.markdown("**Breakfast:** " + ", ".join(diet_info["breakfast"]))
                     if diet_info.get("lunch"): st.markdown("**Lunch:** " + ", ".join(diet_info["lunch"]))
                     # ... etc ...
                     if diet_info.get("weekly_fasting_suggestion"): st.warning(f"**Fasting:** {diet_info['weekly_fasting_suggestion']}")
                     if diet_info.get("timing_notes"): st.markdown(f"**Timing/Notes:** {diet_info['timing_notes']}")
                     if diet_info.get("notes") and not diet_info.get("timing_notes"): st.markdown(f"**Notes:** {diet_info['notes']}")
             elif diet_info.get("notes"): # Only display notes if ONLY notes exist
                  with st.expander("🍎 Dietary Guidelines"):
                     st.markdown(f"{diet_info['notes']}")


        # --- Display Naturopathy ---
        natu_info = advice.get("Naturopathy", {});
        if natu_info and isinstance(natu_info, dict):
             if any(k != "notes" for k in natu_info):
                 with st.expander("💧 Naturopathy & Lifestyle"):
                     # ... (Display Naturopathy details - same as before) ...
                     displayed_practices = False
                     # ... (Loop to display practices/details) ...
                     if natu_info.get("notes"): st.markdown(f"**Overall Notes:** {natu_info['notes']}")
                     if not displayed_practices and natu_info.get("notes"): st.markdown(f"**Notes:** {natu_info['notes']}")
             elif natu_info.get("notes"): # Only display notes if ONLY notes exist
                  with st.expander("💧 Naturopathy & Lifestyle"):
                     st.markdown(f"{natu_info['notes']}")


        # --- Display Ayurveda ---
        ayur_info = advice.get("Ayurveda", {})
        if ayur_info and isinstance(ayur_info, dict):
            if any(k != "notes" for k in ayur_info):
                with st.expander("🌿 Ayurvedic Considerations"):
                    # ... (Display Ayurveda details including disclaimer - same as before) ...
                     if ayur_info.get("lifestyle_principles"): st.markdown("**Lifestyle:** " + ", ".join(ayur_info["lifestyle_principles"]))
                     if ayur_info.get("herbs_decoctions"):
                         # ... (Display herbs + disclaimer) ...
                         st.warning("""**Important Health Advisory:** ... consult ... **Patanjali Chikitsalaya or Megastore** ...""")
                     if ayur_info.get("notes"): st.markdown(f"**Notes:** {ayur_info['notes']}")
            elif ayur_info.get("notes"): # Only display notes if ONLY notes exist
                 with st.expander("🌿 Ayurvedic Considerations"):
                     st.markdown(f"{ayur_info['notes']}")


        # --- Display Pro-Tips ---
        tips_info = advice.get("ProTips", {});
        if tips_info and isinstance(tips_info, dict):
             if any(k != "notes" for k in tips_info):
                 with st.expander("💡 Pro-Tips & Extra Steps"):
                    # ... (Display ProTips details - same as before) ...
                     if tips_info.get("lifestyle"): st.markdown("**Lifestyle/Extra Steps:**\n" + "\n".join([f"- {item}" for item in tips_info["lifestyle"]]))
                     # ... etc ...
                     if tips_info.get("notes"): st.markdown(f"**Notes:** {tips_info['notes']}")
             elif tips_info.get("notes"): # Only display notes if ONLY notes exist
                 with st.expander("💡 Pro-Tips & Extra Steps"):
                     st.markdown(f"{tips_info['notes']}")


    else: # No advice found
        st.info(f"No specific holistic remedy information currently available for {disease} / {severity} / {age_group}.")

    st.markdown("</div>", unsafe_allow_html=True) # Close custom div

# ----------------------------------------------------------------------
# --- END OF PART 1 ---
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# PART 2/3: Page Logic for Diabetes and Heart Disease
# ----------------------------------------------------------------------

# --- SIDEBAR NAVIGATION ---
# ----------------------------------------------------------------------
with st.sidebar:
    selected = option_menu(
        menu_title='HEALTHGUARD',
        options=['Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction'],
        icons=['activity', 'heart-pulse', 'person-badge'],
        menu_icon='hospital-fill',
        default_index=0,
        styles={ # Styling for the sidebar menu
            "container": {"padding": "5px !important", "background-color": "transparent"},
            "icon": {"color": "#FF6347", "font-size": "24px"},
            "nav-link": {"font-size": "17px", "text-align": "left", "margin":"5px", "--hover-color": "#d3e6f5", "border-radius": "5px"},
            "nav-link-selected": {"background-color": "#007bff", "color": "white", "font-weight": "bold"},
        }
     )

# ----------------------------------------------------------------------
# --- PAGE DISPLAY LOGIC ---
# ----------------------------------------------------------------------
# Define severity options
severity_options = ["Mild", "Moderate", "Severe"]

# --- Diabetes Prediction Page ---
if selected == 'Diabetes Prediction':
    st.header('💉 Diabetes Risk Prediction'); st.caption('...')
    with st.form("diabetes_input_form"):
        col1, col2, col3 = st.columns(3)
        # Input Fields
        with col1: Pregnancies = st.text_input('Pregnancies', key='diabetes_preg', help="0 if N/A")
        with col2: Glucose = st.text_input('Glucose (mg/dL)', key='diabetes_gluc')
        with col3: BloodPressure = st.text_input('Diastolic BP (mm Hg)', key='diabetes_bp')
        with col1: SkinThickness = st.text_input('Skin Thickness (mm)', key='diabetes_skin')
        with col2: Insulin = st.text_input('Insulin (mu U/ml)', key='diabetes_insulin')
        with col3: BMI = st.text_input('BMI (kg/m²)', key='diabetes_bmi')
        with col1: DiabetesPedigreeFunction = st.text_input('Pedigree Func.', key='diabetes_dpf', help="Family history value")
        with col2: Age = st.text_input('Age (years)', key='diabetes_age')
        with col3: severity_diabetes = st.selectbox("Perceived Severity:", options=severity_options, key='severity_diabetes', index=1, help="Estimate severity (consult Dr.)")
        submitted_diabetes = st.form_submit_button("Predict Diabetes Risk")

    if submitted_diabetes:
        inputs = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
        if any(x.strip() == "" for x in inputs): st.warning("Please fill in all fields before predicting.")
        else:
            try:
                age_str_diabetes = Age
                if not age_str_diabetes.isdigit() or int(age_str_diabetes) <= 0: raise ValueError("Age must be > 0")
                user_input = [float(x) for x in inputs]
                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person has high risk of diabetes '
                    st.warning(diab_diagnosis, icon="⚠️")
                    display_sanjeevani_advice("Diabetes", age_str_diabetes, severity_diabetes) # Pass severity
                else:
                    diab_diagnosis = 'The person has not risk of diabetes'
                    st.success(diab_diagnosis, icon="✅")
            except ValueError: st.error("Invalid input: Please ensure all fields have valid numbers (Age must be > 0).")
            except Exception as e: st.error(f"An error occurred during prediction: {e}")

    # Doctor Finder Section
    st.markdown("---"); st.subheader("🏥 Find Nearby Doctors & Hospitals")
    selected_city_diabetes = st.selectbox("Select Your City:", options=sorted_cities, key='city_diabetes', index=sorted_cities.index("Kolhapur") if "Kolhapur" in sorted_cities else 0)
    if st.button("Search Nearby Options", key='find_diabetes'):
        user_location_str = city_coordinates.get(selected_city_diabetes)
        if user_location_str:
            with st.spinner(f"Searching options near {selected_city_diabetes}..."):
                 nearest_options = filter_doctors(user_location_str, doctor_data_diabetes)
                 display_doctor_list(nearest_options)
        else: st.error(f"Could not find coordinates for selected city: {selected_city_diabetes}")


# --- Heart Disease Prediction Page ---
elif selected == 'Heart Disease Prediction':
    st.header('❤️ Heart Disease Risk Prediction'); st.caption('...')
    with st.form("heart_input_form"):
        col1, col2, col3 = st.columns(3)
        with col1: age_heart_input = st.number_input('Age (years)', min_value=1, max_value=120, step=1, key='heart_age_input')
        with col2: sex = st.selectbox('Sex', options=[1, 0], format_func=lambda x: 'Male' if x == 1 else 'Female', key='heart_sex')
        with col3: cp = st.selectbox('Chest Pain Type', options=[0, 1, 2, 3], help="0: Typ Ang, 1: Atyp Ang, 2: Non-ang, 3: Asympt", key='heart_cp')
        with col1: trestbps = st.text_input('Resting BP (mm Hg)', key='heart_trestbps')
        with col2: chol = st.text_input('Cholesterol (mg/dl)', key='heart_chol')
        with col3: fbs = st.selectbox('Fasting BS > 120', options=[1, 0], format_func=lambda x: 'Yes' if x == 1 else 'No', key='heart_fbs')
        with col1: restecg = st.selectbox('Resting ECG', options=[0, 1, 2], help="0: Norm, 1: ST-T abnorm, 2: LVH", key='heart_restecg')
        with col2: thalach = st.text_input('Max Heart Rate', key='heart_thalach')
        with col3: exang = st.selectbox('Exercise Angina', options=[1, 0], format_func=lambda x: 'Yes' if x == 1 else 'No', key='heart_exang')
        with col1: oldpeak = st.text_input('ST Depression', key='heart_oldpeak', help="Exercise induced")
        with col2: slope = st.selectbox('Slope ST Seg', options=[0, 1, 2], help="0: Up, 1: Flat, 2: Down", key='heart_slope')
        with col3: ca = st.selectbox('Major Vessels Colored', options=[0, 1, 2, 3], key='heart_ca')
        with col1: thal = st.selectbox('Thalassemia', options=[0, 1, 2, 3], format_func=lambda x: {0:'Unk', 1:'Norm', 2:'Fixed', 3:'Revers'}.get(x, 'Unk'), key='heart_thal')
        with col2: severity_heart = st.selectbox("Perceived Severity:", options=severity_options, key='severity_heart', index=1, help="Estimate condition severity (consult Dr.)")
        submitted_heart = st.form_submit_button("Predict Heart Disease Risk")

    if submitted_heart:
        text_inputs = [trestbps, chol, thalach, oldpeak]
        if any(x.strip() == "" for x in text_inputs) or age_heart_input is None or age_heart_input <= 0:
            st.warning("Please fill in all fields with valid values (Age > 0) before predicting.")
        else:
            try:
                age_heart_str = str(int(age_heart_input))
                user_input = [ float(age_heart_input), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal) ]
                heart_prediction = heart_disease_model.predict([user_input])
                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person has high risk of ** Heart disease **'
                    st.warning(heart_diagnosis, icon="⚠️")
                    display_sanjeevani_advice("Heart Disease", age_heart_str, severity_heart) # Pass severity
                else:
                    heart_diagnosis = 'The person is out of risk'
                    st.success(heart_diagnosis, icon="✅")
            except ValueError: st.error("Invalid input: Ensure all text fields have valid numbers.")
            except Exception as e: st.error(f"An error occurred during prediction: {e}")

    # Doctor Finder Section
    st.markdown("---"); st.subheader("🏥 Find Nearby Doctors & Hospitals")
    selected_city_heart = st.selectbox("Select Your City:", options=sorted_cities, key='city_heart', index=sorted_cities.index("Mumbai") if "Mumbai" in sorted_cities else 0)
    if st.button("Search Nearby Options", key='find_heart'):
        user_location_str = city_coordinates.get(selected_city_heart)
        if user_location_str:
            with st.spinner(f"Searching options near {selected_city_heart}..."):
                 nearest_options = filter_doctors(user_location_str, doctor_data_heart)
                 display_doctor_list(nearest_options)
        else: st.error(f"Could not find coordinates for selected city: {selected_city_heart}")

# ----------------------------------------------------------------------
# --- END OF PART 2 ---
# ----------------------------------------------------------------------
# PART 3/3: Page Logic for Parkinson's and Footer
# ----------------------------------------------------------------------

# --- Parkinson's Prediction Page ---
elif selected == "Parkinsons Prediction":
    st.header("🧠 Parkinson's Disease Risk Prediction")
    st.caption("Enter voice measurement details to predict the risk of Parkinson's disease.")

    with st.form("parkinsons_input_form"):
        age_parkinsons_input = st.number_input('Age (years)', min_value=1, max_value=120, step=1, key='parkinsons_age_input', help="Used for remedy suggestions")
        severity_parkinsons = st.selectbox("Perceived Severity/Stage:", options=severity_options, key='severity_parkinsons', index=1, help="Estimate stage (consult Dr.)")

        st.markdown("###### Voice Measurements")
        col1, col2, col3, col4, col5 = st.columns(5)
        # Parkinson's Voice Input fields
        with col1: fo = st.text_input('MDVP:Fo(Hz)', key='park_fo')
        with col2: fhi = st.text_input('MDVP:Fhi(Hz)', key='park_fhi')
        with col3: flo = st.text_input('MDVP:Flo(Hz)', key='park_flo')
        with col4: Jitter_percent = st.text_input('MDVP:Jitter(%)', key='park_jitter%')
        with col5: Jitter_Abs = st.text_input('MDVP:Jitter(Abs)', key='park_jitterabs')
        with col1: RAP = st.text_input('MDVP:RAP', key='park_rap')
        with col2: PPQ = st.text_input('MDVP:PPQ', key='park_ppq')
        with col3: DDP = st.text_input('Jitter:DDP', key='park_ddp')
        with col4: Shimmer = st.text_input('MDVP:Shimmer', key='park_shimmer')
        with col5: Shimmer_dB = st.text_input('MDVP:Shimmer(dB)', key='park_shimmerdb')
        with col1: APQ3 = st.text_input('Shimmer:APQ3', key='park_apq3')
        with col2: APQ5 = st.text_input('Shimmer:APQ5', key='park_apq5')
        with col3: APQ = st.text_input('MDVP:APQ', key='park_apq')
        with col4: DDA = st.text_input('Shimmer:DDA', key='park_dda')
        with col5: NHR = st.text_input('NHR', key='park_nhr')
        with col1: HNR = st.text_input('HNR', key='park_hnr')
        with col2: RPDE = st.text_input('RPDE', key='park_rpde')
        with col3: DFA = st.text_input('DFA', key='park_dfa')
        with col4: spread1 = st.text_input('spread1', key='park_spread1')
        with col5: spread2 = st.text_input('spread2', key='park_spread2')
        with col1: D2 = st.text_input('D2', key='park_d2')
        with col2: PPE = st.text_input('PPE', key='park_ppe')

        submitted_parkinsons = st.form_submit_button("Predict Parkinson's Risk")

    if submitted_parkinsons:
        inputs = [fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
        # Check age explicitly
        if any(x.strip() == "" for x in inputs) or age_parkinsons_input is None or age_parkinsons_input <=0:
            st.warning("Please fill in all fields (including Age > 0) before predicting.")
        else:
            try:
                age_parkinsons_str = str(int(age_parkinsons_input))
                user_input_model = [float(x) for x in inputs] # Model inputs
                parkinsons_prediction = parkinsons_model.predict([user_input_model])

                if parkinsons_prediction[0] == 1:
                    parkinsons_diagnosis = "Based on voice inputs, patterns consistent with **Parkinson's disease** are indicated..."
                    st.warning(parkinsons_diagnosis, icon="⚠️")
                    display_sanjeevani_advice("Parkinsons", age_parkinsons_str, severity_parkinsons) # Pass severity
                else:
                    parkinsons_diagnosis = "Based on voice inputs, patterns consistent with Parkinson's disease were **not indicated**."
                    st.success(parkinsons_diagnosis, icon="✅")
            except ValueError: st.error("Invalid input: Ensure all voice measurement fields contain only valid numbers.")
            except Exception as e: st.error(f"An error occurred during prediction: {e}")

    # Doctor Finder Section
    st.markdown("---"); st.subheader("🏥 Find Nearby Doctors & Hospitals")
    selected_city_parkinsons = st.selectbox("Select Your City:", options=sorted_cities, key='city_parkinsons', index=sorted_cities.index("Mumbai") if "Mumbai" in sorted_cities else 0)
    if st.button("Search Nearby Options", key='find_parkinsons'):
        user_location_str = city_coordinates.get(selected_city_parkinsons)
        if user_location_str:
            with st.spinner(f"Searching options near {selected_city_parkinsons}..."):
                 nearest_options = filter_doctors(user_location_str, doctor_data_parkinsons)
                 display_doctor_list(nearest_options)
        else: st.error(f"Could not find coordinates for selected city: {selected_city_parkinsons}")

# ----------------------------------------------------------------------
# --- FOOTER / DISCLAIMER ---
# ----------------------------------------------------------------------
st.markdown("---")
st.caption("© HealthGuard - Sanjeevani Holistic Remedy Companion | Disclaimer: Predictions and remedies are informational and for dealing with root cause as per our best knowledge. Severity selection is subjective. Consult qualified professionals for medical advice. Verify hospital/doctor data independently.")
# ----------------------------------------------------------------------
# --- END OF PART 3 ---
# ----------------------------------------------------------------------