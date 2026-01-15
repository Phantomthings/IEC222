from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates

from config import SYNOPTIQUE_VARIABLES
from routers.synoptique_config import MODULES, POLE_GROUPES, CONTACTEURS_KM, PDC_STATUS_LIST

router = APIRouter()
templates = Jinja2Templates(directory="templates")


COLORS = {
    "off": "#525252",
    "on": "#22c55e", 
    "charging": "#09bfec",
    "warning": "#eab308",
    "fault": "#ef4444",
    "contact_open": "#f59e0b",
    "contact_closed": "#22c55e",
    "border_off": "#334155",
    "border_on": "#22c55e",
    "coil_off": "#64748b",
    "coil_on": "#22c55e",
}


def status_color(status: int) -> str:
    return {
        0: COLORS["off"],
        1: COLORS["on"],
        2: COLORS["charging"],
        3: COLORS["fault"],
    }.get(int(status or 0), COLORS["off"])


def module_status_color(status: int) -> str:
    return {
        2: "#f70000",
        6: "#c0ffc0",
    }.get(int(status or 0), COLORS["off"])


def pole_groupe_status_color(status: int) -> str:
    if status in [0, 1]:
        return "url(#glowWhite)"
    elif status in [2, 3]:
        return "url(#glowGroupGreen)"
    elif status == 4:
        return "url(#glowGroupRed)"
    return "url(#panelGrad)"


def contacteur_state(status: int) -> dict:
    is_closed = status == 6
    is_open = status == 2
    is_fault = status == 17
    is_not_ready = status == 1
    
    if is_fault:
        border_color = COLORS["fault"]
        contact_color = COLORS["fault"]
        led_color = COLORS["fault"]
        led_filter = "url(#glowOrange)"
    elif is_closed:
        border_color = COLORS["border_on"]
        contact_color = COLORS["contact_closed"]
        led_color = COLORS["on"]
        led_filter = "url(#glowGreen)"
    elif is_open:
        border_color = COLORS["border_off"]
        contact_color = COLORS["contact_open"]
        led_color = COLORS["off"]
        led_filter = "none"
    else:
        border_color = COLORS["off"]
        contact_color = COLORS["off"]
        led_color = COLORS["off"]
        led_filter = "none"
    
    return {
        "is_closed": is_closed,
        "border_color": border_color,
        "contact_color": contact_color,
        "contact_x2": "0" if is_closed else "12",
        "contact_y2": "24" if is_closed else "20",
        "led_color": led_color,
        "led_filter": led_filter,
    }


def contacteur_kp_state(status: int) -> dict:
    is_closed = status == 6
    is_open = status == 2
    is_fault = status == 17
    is_not_ready = status == 1
    
    if is_fault:
        border_color = COLORS["fault"]
        contact_color = COLORS["fault"]
        fixed_color = COLORS["fault"]
        coil_color = COLORS["fault"]
        led_color = COLORS["fault"]
        led_filter = "url(#glowOrange)"
    elif is_closed:
        border_color = COLORS["border_on"]
        contact_color = COLORS["contact_closed"]
        fixed_color = COLORS["contact_closed"]
        coil_color = COLORS["coil_on"]
        led_color = COLORS["on"]
        led_filter = "url(#glowGreen)"
    elif is_open:
        border_color = COLORS["border_off"]
        contact_color = COLORS["contact_open"]
        fixed_color = COLORS["contact_open"]
        coil_color = COLORS["coil_off"]
        led_color = COLORS["off"]
        led_filter = "none"
    else:
        border_color = COLORS["off"]
        contact_color = COLORS["off"]
        fixed_color = COLORS["off"]
        coil_color = COLORS["off"]
        led_color = COLORS["off"]
        led_filter = "none"
    
    return {
        "is_closed": is_closed,
        "border_color": border_color,
        "contact_color": contact_color,
        "contact_x2": "0" if is_closed else "15",
        "contact_y2": "33" if is_closed else "28",
        "fixed_color": fixed_color,
        "coil_color": coil_color,
        "led_color": led_color,
        "led_filter": led_filter,
    }

def pdc_state(color_status: int, text_status: str) -> dict:
    color = status_color(color_status)
    
    text_color = "#052e16" if color_status == 1 else "#422006" if color_status == 3 else "#ffffff"
    glow_filter = {
        1: "url(#glowGreen)",
        2: "url(#glowCyan)",
        3: "url(#glowOrange)",
    }.get(color_status, "none")
    
    return {
        "color": color,
        "text": text_status,
        "text_color": text_color,
        "glow_filter": glow_filter,
    }
@router.get("/synoptique", response_class=HTMLResponse)
async def synoptique_page(request: Request):
    return templates.TemplateResponse("synoptique.html", {"request": request})


async def load_data() -> dict:
    from main import get_opcua_client
    import asyncio
    
    opcua = get_opcua_client()
    
    tasks = {key: opcua.read_variable(node_id) for key, node_id in SYNOPTIQUE_VARIABLES.items()}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    
    data = {}
    for key, result in zip(tasks.keys(), results):
        if isinstance(result, Exception):
            data[key] = 0
        else:
            data[key] = result

    for i in range(1, 15):
        m = MODULES[f"M{i}"]
        m.vdc = data.get(f"m{i}_vdc", 0.0)
        m.idc = data.get(f"m{i}_idc", 0.0)
        m.status = data.get(f"m{i}_status", 0)

    for i in range(1, 11):
        pg = POLE_GROUPES[f"G{i}"]
        pg.status = data.get(f"pg{i}_status", 0)
        pg.color_id = data.get(f"pg{i}_color_id", -1)
        pg.id_prise = data.get(f"pg{i}_id_prise", 0)

    for i in range(1, 13):
        km = CONTACTEURS_KM[f"K{i}"]
        km.status = data.get(f"km{i}_status", 0)

    for i in range(1, 5):
        pdc = PDC_STATUS_LIST[f"PDC{i}"]
        pdc.color_status = data.get(f"pdc{i}_color_status", 0)
        pdc.text_status = data.get(f"pdc{i}_text_status", "")
    
    for i in range(1, 5):
        pdc = PDC_STATUS_LIST[f"PDC{i}"]
        pdc.color_status = data.get(f"pdc{i}_color_status", 0)
        pdc.text_status = data.get(f"pdc{i}_text_status", "")
        pdc.px_current = data.get(f"px_current_pdc{i}", 0.0)
        pdc.px_voltage = data.get(f"px_voltage_pdc{i}", 0.0)
        pdc.evi_voltage = data.get(f"evi_voltage_pdc{i}", 0.0)
        pdc.dcbm_voltage = data.get(f"dcbm_voltage_pdc{i}", 0.0)
        pdc.px_power = data.get(f"px_power_pdc{i}", 0.0)
        pdc.nb_mxr_available = data.get(f"nb_mxr_available_pdc{i}", 0)
        pdc.nb_mxr_running = data.get(f"nb_mxr_running_pdc{i}", 0)

    return data

@router.get("/synoptique/fullscreen", response_class=HTMLResponse)
async def synoptique_fullscreen(request: Request):
    return templates.TemplateResponse("synoptique_fullscreen.html", {"request": request})
@router.get("/api/synoptique/data")
async def get_synoptique_data():
    try:
        data = await load_data()
        
        result = {}
        
        for i in range(1, 15):
            m = MODULES[f"M{i}"]
            result[f"M{i}"] = {
                "vdc": round(m.vdc, 0),
                "idc": round(m.idc, 0),
                "status": m.status,
                "module_color": module_status_color(m.status),
            }
        
        for i in range(1, 11):
            pg = POLE_GROUPES[f"G{i}"]
            result[f"G{i}"] = {
                "glow_filter": pole_groupe_status_color(pg.status),
                "id_prise": pg.id_prise,
            }
        
        for i in range(1, 13):
            km = CONTACTEURS_KM[f"K{i}"]
            result[f"K{i}"] = contacteur_state(km.status)
        
        for i in range(1, 5):
            kp_status = data.get(f"p{i}_status", 0)
            result[f"KP{i}"] = contacteur_kp_state(kp_status)
        
        for i in range(1, 5):
            pdc = PDC_STATUS_LIST[f"PDC{i}"]
            pdc_data = pdc_state(pdc.color_status, pdc.text_status)
            pdc_data.update({
                "px_current": round(data.get(f"px_current_pdc{i}", 0.0), 1),
                "px_voltage": round(data.get(f"px_voltage_pdc{i}", 0.0), 1),
                "evi_voltage": round(data.get(f"evi_voltage_pdc{i}", 0.0), 1),
                "dcbm_voltage": round(data.get(f"dcbm_voltage_pdc{i}", 0.0), 1),
                "px_power": round(data.get(f"px_power_pdc{i}", 0.0), 1),
                "nb_mxr_available": int(data.get(f"nb_mxr_available_pdc{i}", 0)),
                "nb_mxr_running": int(data.get(f"nb_mxr_running_pdc{i}", 0)),
            })
            result[f"PDC{i}"] = pdc_data
        
        return JSONResponse(result)
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)