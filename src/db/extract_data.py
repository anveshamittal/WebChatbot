import pyodbc
import os

def fetch_data():
    # conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};Server=DESKTOP-VAR056C\\SQLEXPRESS;Database=mydatabase;UID=sa;PWD=A1m13i9t20@@;TrustServerCertificate=Yes;")
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Products")
    # rows = cursor.fetchall()
    # return [{"title": r.ProductName, "body": r.UnitPrice, "url": r.UnitsOnOrder} for r in rows]
    return """
The Whisper of the Aetherbloom
The air in the Whispering Peaks was always thin, carrying with it the scent of ancient pine and the faint, metallic tang of the Aetherbloom. Elara, a girl whose hair was the color of twilight and whose eyes held the deep blue of mountain lakes, knew this scent better than any other. She had spent her seventeen years nestled in the shadow of the tallest peak, Mount Cinder, where the legendary Aetherbloom was said to grow. Not just any flower, but one that pulsed with the very essence of the world's magic, blooming only once a century, and then, only for a single night.

This year was the year. The elders had spoken of it in hushed tones, their faces etched with a mixture of reverence and fear. The last blooming had brought a great healing to their village after a devastating blight, but it had also drawn creatures from the shadowed valleys, hungry for its power. Elara, however, felt no fear, only a profound sense of destiny. Her grandmother, a wise woman with hands like gnarled roots and eyes that saw more than the visible, had told her stories of the Aetherbloom since she was a child. "It calls to those with pure hearts, little star," she'd whispered, tracing patterns on Elara's palm. "And your heart, it shines."

As the sun dipped below the jagged horizon, painting the sky in fiery hues of orange and purple, a soft, ethereal glow began to emanate from the highest, most inaccessible crag of Mount Cinder. It was a light unlike any other, not harsh like fire, nor cold like moonlight, but a warm, pulsating luminescence that seemed to hum with silent energy. The Aetherbloom.

Elara had prepared for this night for weeks. She wore her sturdiest boots, a thick wool cloak against the mountain chill, and carried a small, worn leather satchel containing a dried herb poultice and a crystal shard, a gift from her grandmother. While the rest of the village huddled in their homes, chanting protective wards, Elara slipped out, her heart a drum against her ribs.

The climb was arduous. The path, barely more than a goat track, wound precariously along sheer cliffs. Loose scree shifted underfoot, and the wind howled like a hungry beast, trying to tear her from the mountain face. But Elara pressed on, driven by an unseen force, the Aetherbloom's glow growing ever brighter, a beacon in the encroaching darkness. She could feel its magic now, a gentle thrumming beneath her skin, guiding her steps.

Hours later, breathless and with aching muscles, she reached a small, hidden plateau near the summit. And there it was.

The Aetherbloom wasn't a single flower, but a cluster of delicate, translucent blossoms, each petal shimmering with an inner light. They pulsed in unison, casting a soft, otherworldly glow on the surrounding rocks. The air around them vibrated with an almost audible hum, a symphony of ancient magic. It was more beautiful, more powerful, than any story had ever described.

As Elara knelt before it, a shadow detached itself from the deeper gloom of the mountain. It was a creature of jagged edges and predatory grace, its eyes like chips of obsidian, its form vaguely lupine but far more ancient and menacing. A Shadow-Hound, drawn by the bloom's power, just as the elders had feared. It snarled, a low, guttural sound that echoed through the stillness, its gaze fixed on the glowing flowers.

Fear, cold and sharp, pierced through Elara. But then, she remembered her grandmother's words: "It calls to those with pure hearts." She looked at the Aetherbloom, then back at the snarling beast. The creature was not evil, she realized, but simply drawn to the magic, perhaps even suffering from its absence.

Taking a deep breath, Elara reached into her satchel and pulled out the crystal shard. It was a piece of clear quartz, imbued with her grandmother's gentle magic. Holding it aloft, she focused, not on fighting the creature, but on the connection she felt to the Aetherbloom, to the mountain, to the very essence of life. She began to hum, a low, melodic tune her grandmother had taught her, a song of peace and healing.

The Shadow-Hound paused, its snarl faltering. The Aetherbloom seemed to respond, its pulses growing stronger, its light expanding, enveloping Elara and the creature in a soft, warm embrace. The crystal in Elara's hand glowed, reflecting the bloom's light, amplifying her intent. The creature, bathed in the gentle magic, whimpered, its rigid form softening, its obsidian eyes losing their harshness. It lay down, no longer a threat, but a weary soul seeking solace.

Elara understood. The Aetherbloom's power wasn't just for healing the physical, but for soothing the spirit. She gently touched one of the glowing petals. A surge of pure, raw energy flowed into her, not overwhelming, but harmonious, like a river finding its path to the sea. She felt connected to everything, to the mountain, the sky, the very stars above.

As the first hint of dawn painted the eastern sky, the Aetherbloom's light began to dim, its petals slowly folding inward, preparing for its century-long slumber. The Shadow-Hound, now calm and still, faded back into the shadows, leaving only a faint impression on the dewy ground.

Elara descended the mountain as the sun rose, a new light in her eyes. She carried no physical bloom, but the whisper of the Aetherbloom resonated within her, a profound understanding of the world's delicate balance, and the quiet power of a pure heart. The village awoke to a new day, unaware of the night's silent magic, but Elara knew. She carried the Aetherbloom's legacy, not as a guardian of a flower, but as a keeper of its whisper, ready to share its message of healing and harmony with her people, one gentle act at a time."""
 
docs=fetch_data()
