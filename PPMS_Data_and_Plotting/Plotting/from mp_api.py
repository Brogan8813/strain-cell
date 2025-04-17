from mp_api.client import MPRester
with MPRester(api_key="login_for_your_api_key") as mpr:
    data = mpr.materials.search(material_ids=["mp-22850"])