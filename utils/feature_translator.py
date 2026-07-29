# utils/feature_translator.py

def translate(features, final_url):

    uci = {}

    # Direct mappings
    uci["having_IP_Address"] = int(
        features["has_ip_address"]
    )

    uci["URL_Length"] = int(
        features["url_length"]
    )

    uci["Prefix_Suffix"] = int(
        features["hyphen_count"] > 0
    )

    uci["having_Sub_Domain"] = int(
        features["subdomain_count"]
    )

    # URL checks
    uci["having_At_Symbol"] = int(
        "@" in final_url
    )

    uci["double_slash_redirecting"] = int(
        "//" in final_url[8:]
    )

    uci["HTTPS_token"] = int(
        "https" in final_url
        .replace("https://", "")
    )

    # Website content mappings
    uci["Request_URL"] = int(
        features["image_count"] > 20
    )

    uci["URL_of_Anchor"] = int(
        features["form_count"] > 0
    )

    uci["Links_in_tags"] = int(
        features["script_count"] > 20
    )

    # Threat indicators
    uci["Google_Index"] = int(
        features["search_domain_frequency"] > 0
    )

    uci["Abnormal_URL"] = int(
        not features["official_domain_match"]
    )

    # Unknown for now
    uci["Shortining_Service"] = 0
    uci["SSLfinal_State"] = 0
    uci["Domain_registeration_length"] = 0
    uci["Favicon"] = 0
    uci["port"] = 0
    uci["SFH"] = 0
    uci["Submitting_to_email"] = 0
    uci["Redirect"] = 0
    uci["on_mouseover"] = 0
    uci["RightClick"] = 0
    uci["popUpWidnow"] = 0
    uci["Iframe"] = 0
    uci["age_of_domain"] = 0
    uci["DNSRecord"] = 0
    uci["web_traffic"] = 0
    uci["Page_Rank"] = 0
    uci["Links_pointing_to_page"] = 0
    uci["Statistical_report"] = 0

    return uci