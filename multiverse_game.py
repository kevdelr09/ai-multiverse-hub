import streamlit as st
import json
import os
import random
from groq import Groq

# 1. SET YOUR FREE GROQ API KEY HERE
API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=API_KEY)
SAVE_FILE = "multiverse_save.json"

st.set_page_config(page_title="AI Adventure Hub", layout="centered")
st.title("🎮 Infinite AI Adventure Hub")



# --- INITIALIZE SESSION DATA ---

    
if "messages" not in st.session_state:
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            st.session_state.last_voice_input = ""
            saved_data = json.load(file)
            st.session_state.messages = saved_data.get("messages", [])
            st.session_state.current_image_prompt = saved_data.get("current_image_prompt", "landscape")
            st.session_state.health = saved_data.get("health", 100)
            st.session_state.inventory = saved_data.get("inventory", "")
            st.session_state.genre = saved_data.get("genre", "")
            st.session_state.last_voice_input = ""
    else:
        st.session_state.messages = []
        st.session_state.current_image_prompt = "landscape"
        st.session_state.health = 100
        st.session_state.inventory = ""
        st.session_state.genre = ""

def save_game_state():
    state_data = {
        "messages": st.session_state.messages,
        "current_image_prompt": st.session_state.current_image_prompt,
        "health": st.session_state.health,
        "inventory": st.session_state.inventory,
        "genre": st.session_state.genre
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(state_data, file)

# --- MAIN MENU & GENRE SELECTION ---
if not st.session_state.messages:
    st.subheader("Choose Your Adventure Pathway:")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⚔️ Classical RPG\n(Fantasy & Loot)"):
            st.session_state.genre = "rpg"
            locs = ["a flooded cavern", "a haunted graveyard", "a bustling pirate tavern"]
            chosen = random.choice(locs)
            st.session_state.inventory = "Iron Sword, Rations"
            st.session_state.health = 100
            st.session_state.messages = [{
                "role": "system", 
                "content": f"You are a classic Fantasy RPG Game Master. Describe a starting area. You MUST start the player in {chosen}. Keep descriptions under 4 sentences. Always end by asking 'What do you do next?'. CRITICAL: At the very end of your response, on a completely new line, you MUST write '[IMAGE]:' followed by a short, descriptive 1-sentence prompt for a fantasy digital painting representing this scene."
            }]
            st.session_state.current_image_prompt = chosen
            save_game_state()
            st.rerun()
    
    with col2:
        if st.button("🎒 Kids Learning\n(Fun Puzzles)"):
            st.session_state.genre = "kids"
            locs = ["The Addition Arithmetic Castle", "The Alphabet Jungle Safari"]
            chosen = random.choice(locs)
            st.session_state.inventory = "Magic Pencil, Star Stickers"
            st.session_state.health = 100
            st.session_state.messages = [{
                "role": "system", 
                "content": f"You are a friendly, encouraging AI Teacher in a magical educational video game. Describe a starting area. You MUST start the child in {chosen}. Keep descriptions under 4 sentences using enthusiastic language for a 7-year-old child. Every single turn, you must include a simple math puzzle, word rhyme, or science fact question for the child to answer. Always end by asking 'or What do you want to try next?'. CRITICAL: At the very end of your response, on a completely new line, you MUST write '[IMAGE]:' followed by a short, descriptive 1-sentence prompt for a bright, whimsical, cute 3D cartoon Pixar-style animation illustration representing this scene."
            }]
            st.session_state.current_image_prompt = chosen
            save_game_state()
            st.rerun()

    with col3:
        if st.button("🍳 Cooking Challenge\n(Kitchen Simulator)"):
            st.session_state.genre = "cooking"
            locs = ["a Michelin Star restaurant kitchen", "a cozy grandmother's bakery"]
            chosen = random.choice(locs)
            st.session_state.inventory = "Chef's Knife, Frying Pan"
            st.session_state.health = 100
            st.session_state.messages = [{
                "role": "system", 
                "content": (
                    f"You are a strict Celebrity Head Chef running a realistic, step-by-step culinary simulation. "
                    f"You MUST start the player in {chosen} and assign them a specific dish to cook. "
                    "You must guide them through the real chronological cooking process step-by-step. "
                    "Every turn must directly evaluate their previous choice. If they overcook, under-season, or miss a step, describe the culinary failure and deduct quality points. "
                    "Only advance to the next step of the recipe (e.g., moving from prepping ingredients to heat control) if their choice makes sense. "
                    "Keep responses under 4 sentences. Always end by asking: 'What is your next culinary move, Chef?' "
                    "If they make a bad culinary decision, "
                    "overcook, or mismanage tools, you MUST start your sentence with the word 'WRONG!' or 'FAILED!'. "
                    "Keep responses under 4 sentences. Always end by asking: 'What is your next culinary move, Chef?' "
                    "CRITICAL: At the very end of your response, on a completely new line, you MUST write '[IMAGE]:' followed by a short, descriptive 1-sentence prompt representing the current stage of this dish."
                )
            }]
            st.session_state.current_image_prompt = chosen
            save_game_state()
            st.rerun()
    st.markdown("---")
    if os.path.exists(SAVE_FILE):
        if st.button("💾 Resume Your Previous Saved Adventure"):
            st.rerun()
    with col4:
        st.write("✨ **Custom Sandbox**")
        custom_topic = st.text_input("Enter any theme / topic:", placeholder="e.g., Zombie Outbreak, Cyberpunk...", key="sandbox_input")
        if st.button("🚀 Launch Sandbox") and custom_topic:
            st.session_state.genre = f"custom: {custom_topic}"
            st.session_state.inventory = "Basic Supplies, Map"
            st.session_state.health = 100
            st.session_state.messages = [{
                "role": "system", 
                "content": (
                    f"You are an expert AI Simulator running a text adventure game set entirely within the theme: '{custom_topic}'. "
                    "Describe a starting area relevant to this topic under 4 sentences. Make it immersive, capturing the precise mood of this world. "
                    "Incorporate resource management, health metrics, and branching scenarios based entirely on what the player choices dictate. "
                    "Always end your responses by asking: 'What do you do next?' "
                    "CRITICAL: At the very end of your response, on a completely new line, you MUST write '[IMAGE]:' followed by a short, descriptive 1-sentence prompt for a realistic, cinematic, high-detailed 8k render snapshot capturing this specific thematic environment."
                )
            }]
            st.session_state.current_image_prompt = custom_topic
            save_game_state()
            st.rerun()
# --- ACTIVE GAME INTERFACE ---
else:
    # 4. EXECUTE AI ENGINE FIRST IF NEEDED (Moved up to fix the start glitch!)
    if st.session_state.messages[-1]["role"] in ["system", "user"]:
        with st.spinner("The AI Engine is processing..."):
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            raw_c = res.choices[0].message.content
            
            if "damage" in raw_c.lower() or "wrong" in raw_c.lower() or "burned" in raw_c.lower():
                st.session_state.health = max(0, st.session_state.health - 10)
            if "heal" in raw_c.lower() or "correct" in raw_c.lower() or "perfect" in raw_c.lower():
                st.session_state.health = min(100, st.session_state.health + 10)
            
            img_p = st.session_state.current_image_prompt
            if "[IMAGE]:" in raw_c:
                parts = raw_c.split("[IMAGE]:")
                raw_c = parts[0].strip()
                img_p = parts[1].strip()
            elif "[IMAGE]" in raw_c:
                parts = raw_c.split("[IMAGE]")
                raw_c = parts[0].strip()
                img_p = parts[1].strip()
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": raw_c,
                "image_prompt": img_p
            })
            st.session_state.current_image_prompt = img_p
            save_game_state()
            st.rerun()

    with st.sidebar:
        st.header("📊 Status Panel")
        if st.session_state.genre == "kids":
            st.metric(label="⭐ Brain Power Points", value=f"{st.session_state.health} / 100")
            st.progress(st.session_state.health / 100)
            st.text_area("🎒 Backpack Items", value=st.session_state.inventory, disabled=True)
        elif st.session_state.genre == "cooking":
            st.metric(label="⏱️ Dish Quality Rating", value=f"{st.session_state.health}% Perfect")
            st.progress(st.session_state.health / 100)
            st.text_area("🔪 Kitchen Pantry", value=st.session_state.inventory, disabled=True)
        else:
            st.metric(label="❤️ Health Points", value=f"{st.session_state.health} / 100")
            st.progress(st.session_state.health / 100)
            st.text_area("🎒 RPG Inventory", value=st.session_state.inventory, disabled=True)
        
        st.markdown("---")
        if st.button("💥 Return to Main Menu (Wipe Save)"):
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            st.session_state.clear()
            st.rerun()


    # 1. FIXED IMAGE BLOCK: Clean string completely and bypass local code loading
    # We clean text brackets out so the raw web address never fractures
    raw_prompt = str(st.session_state.current_image_prompt)
    clean_prompt = raw_prompt.replace("[IMAGE]:", "").replace("[IMAGE]", "").replace(" ", "%20").strip()
    
    # Generate unique layout index link
    final_image_url = f"https://image.pollinations.ai/p/{clean_prompt},%20fantasy%20rpg%20digital%20painting?width=800&height=450&seed=15"
    
    # Pass directly to browser via Streamlit's native URL viewer layout
    st.image(final_image_url, use_container_width=True)

    # 2. SCROLLABLE LOG BOX & NARRATION
            # 2. SCROLLABLE LOG BOX & NARRATION
    st.markdown("### 📜 The Experience Log")
    chat_container = st.container(height=300)
    
    with chat_container:
        total_m = len(st.session_state.messages)
        for idx, msg in enumerate(st.session_state.messages):
            if msg["role"] == "assistant":
                
                # 🛠️ AGGRESSIVE TEXT SCRUBBER (Fixes Sandbox Narration)
                # This guarantees we extract pure story text string without tag corruption
                raw_text = str(msg["content"])
                clean_t = raw_text
                
                # Checks every possible way the AI could spell the image tracking phrase
                tags_to_check = ["[IMAGE]:", "[IMAGE]", "[image]:", "[image]", "image:", "IMAGE:"]
                for current_tag in tags_to_check:
                    if current_tag in raw_text:
                        clean_t = raw_text.split(current_tag)[0].strip()
                        break
                
                # Render the clean text bubble on your layout canvas
                st.chat_message("assistant", avatar="👩‍🏫" if st.session_state.genre == "kids" else "🧙‍♂️").write(clean_t)
                
                # 🎙️ AUDIO NARRATOR ENGINE (Forced to process pure string variables)
                if idx == total_m - 1:
                    safe_narr = clean_t.replace('"', '\\"').replace("'", "\\'").replace('\n', ' ')
                    
                    # Uses enthusiastic voice settings for kids tutor, standard for others
                    pitch_val = 1.1 if st.session_state.genre == "kids" else 0.85
                    rate_val = 1.0 if st.session_state.genre == "kids" else 0.95
                    
                    st.components.v1.html(
                        f"""
                        <script>
                        window.parent.speechSynthesis.cancel(); 
                        var msg = new SpeechSynthesisUtterance("{safe_narr}"); 
                        msg.rate = {rate_val}; 
                        msg.pitch = {pitch_val}; 
                        window.parent.speechSynthesis.speak(msg);
                        </script>
                        """,
                        height=0
                    )
            elif msg["role"] == "user":
                st.chat_message("user", avatar="⚔️" if st.session_state.genre == "rpg" else "🧑‍🍳").write(msg["content"])

        

       # 3. INTERACTIVE INPUT CONTROLLER (With instant clear callback & instant sync!)
    
    # Define a clean callback function at the input frame level to wipe data on enter
    def clear_text_input():
        if st.session_state.text_move_box:
            st.session_state.messages.append({"role": "user", "content": st.session_state.text_move_box})
            save_game_state()
        st.session_state.text_move_box = "" # Forces the input layout to render blank

    # Text input option with clear callback attached
    st.text_input(
        "Type your move here...", 
        placeholder="Type an action and hit Enter...", 
        key="text_move_box",
        on_change=clear_text_input
    )

    # Voice mic controller block
    audio_file = st.audio_input("Or speak your move here... Press Stop after saying your answer")
    
    if audio_file is not None:
        with st.spinner("🎙️ Transcribing your voice..."):
            try:
                audio_bytes = audio_file.read()
                transcription = client.audio.transcriptions.create(
                    file=("voice.wav", audio_bytes, "audio/wav"),
                    model="whisper-large-v3",
                    response_format="text"
                )
                spoken_text = str(transcription).strip()
                
                if spoken_text and spoken_text != st.session_state.get("last_voice_input", ""):
                    st.session_state.last_voice_input = spoken_text
                    st.session_state.messages.append({"role": "user", "content": spoken_text})
                    save_game_state()
                    # Instantly force a page rerun so the history log displays your spoken words immediately
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Voice Transcription failed: {e}")

