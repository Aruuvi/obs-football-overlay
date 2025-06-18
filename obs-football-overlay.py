import obspython as obs
import time

scores = {"Team1": 0, "Team2": 0}
text_sources = {"Team1": "", "Team2": ""}

timer_source = ""
timer_running = False
timer_start_time = 0
timer_elapsed = 0

max_time_seconds = 12 * 60  # Default to 12 minutes

def is_text_source(source_id):
    return source_id in ["text_gdiplus", "text_ft2_source", "text_v2"]

def update_score_text(team):
    source_name = text_sources.get(team, "")
    if not source_name:
        return
    source = obs.obs_get_source_by_name(source_name)
    if source:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", str(scores[team]))
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

def update_timer_text():
    if not timer_source:
        return
    minutes = int(timer_elapsed // 60)
    seconds = int(timer_elapsed % 60)
    time_str = f"{minutes:02d}:{seconds:02d}"
    source = obs.obs_get_source_by_name(timer_source)
    if source:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", time_str)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.obs_source_release(source)

def update_all_sources():
    for team in scores:
        update_score_text(team)
    update_timer_text()

def increase_score(team):
    scores[team] += 1
    update_score_text(team)

def decrease_score(team):
    if scores[team] > 0:
        scores[team] -= 1
        update_score_text(team)

def reset_scores():
    for team in scores:
        scores[team] = 0
    update_all_sources()

def start_timer():
    global timer_running, timer_start_time
    if not timer_running:
        timer_start_time = time.time() - timer_elapsed
        timer_running = True

def stop_timer():
    global timer_running, timer_elapsed
    if timer_running:
        timer_elapsed = time.time() - timer_start_time
        timer_running = False

def reset_timer():
    global timer_elapsed, timer_running
    timer_elapsed = 0
    timer_running = False
    update_timer_text()

def timer_tick():
    global timer_elapsed, timer_running
    if timer_running:
        timer_elapsed = time.time() - timer_start_time
        if timer_elapsed >= max_time_seconds:
            timer_elapsed = max_time_seconds
            timer_running = False
    update_timer_text()

def script_description():
    return (
        "OBS script for displaying scores and a custom-length match timer."
        "\n- Select text sources for both teams and the timer."
        "\n- Increase or decrease team scores."
        "\n- Start, stop, or reset the timer."
        "\n- The timer stops automatically after the specified match duration."
    )

def script_properties():
    props = obs.obs_properties_create()

    sources = obs.obs_enum_sources()
    list_sources = {}

    if sources:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            if is_text_source(source_id):
                name = obs.obs_source_get_name(source)
                list_sources[name] = name
        obs.source_list_release(sources)

    def add_source_selector(prop_id, label):
        p = obs.obs_properties_add_list(props, prop_id, label, obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
        obs.obs_property_list_add_string(p, "", "")
        for key in sorted(list_sources):
            obs.obs_property_list_add_string(p, key, key)

    add_source_selector("Team1_source", "Text Source - Team 1")
    add_source_selector("Team2_source", "Text Source - Team 2")
    add_source_selector("Timer_source", "Text Source - Timer")

    obs.obs_properties_add_int(props, "match_duration", "Match Duration (minutes)", 1, 120, 1)

    obs.obs_properties_add_button(props, "refresh", "🔄 Refresh", lambda props, prop: (update_all_sources(), False)[1])
    obs.obs_properties_add_button(props, "add_team1", "➕ Goal for Team 1", lambda props, prop: (increase_score("Team1"), False)[1])
    obs.obs_properties_add_button(props, "remove_team1", "➖ Remove Goal from Team 1", lambda props, prop: (decrease_score("Team1"), False)[1])
    obs.obs_properties_add_button(props, "add_team2", "➕ Goal for Team 2", lambda props, prop: (increase_score("Team2"), False)[1])
    obs.obs_properties_add_button(props, "remove_team2", "➖ Remove Goal from Team 2", lambda props, prop: (decrease_score("Team2"), False)[1])
    obs.obs_properties_add_button(props, "reset_scores", "🔄 Reset Scores", lambda props, prop: (reset_scores(), False)[1])

    obs.obs_properties_add_button(props, "start_timer", "▶️ Start Timer", lambda props, prop: (start_timer(), False)[1])
    obs.obs_properties_add_button(props, "stop_timer", "⏸️ Stop Timer", lambda props, prop: (stop_timer(), False)[1])
    obs.obs_properties_add_button(props, "reset_timer", "🔄 Reset Timer", lambda props, prop: (reset_timer(), False)[1])

    return props

def script_update(settings):
    global text_sources, timer_source, max_time_seconds
    text_sources["Team1"] = obs.obs_data_get_string(settings, "Team1_source")
    text_sources["Team2"] = obs.obs_data_get_string(settings, "Team2_source")
    timer_source = obs.obs_data_get_string(settings, "Timer_source")
    match_duration = obs.obs_data_get_int(settings, "match_duration")
    max_time_seconds = match_duration * 60
    update_all_sources()

def script_save(settings):
    for key in text_sources:
        obs.obs_data_set_string(settings, key + "_source", text_sources.get(key, ""))
    obs.obs_data_set_string(settings, "Timer_source", timer_source)
    obs.obs_data_set_int(settings, "match_duration", max_time_seconds // 60)

def script_load(settings):
    obs.timer_add(timer_tick, 1000)

def script_unload():
    obs.timer_remove(timer_tick)
