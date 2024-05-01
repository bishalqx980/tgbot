from bot import g4f

class G4F:
    async def chatgpt(prompt):
        try:
            response = g4f.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            response = response.choices[0].message.content
            return response
        except Exception as e:
            print(f"Error g4f_chatgpt: {e}")


    async def imagine(prompt):
        try:
            response = g4f.images.generate(
            model="gemini",
            prompt=prompt
            )
            image_url = response.data[0].url
            return image_url
        except Exception as e:
            print(f"Error g4f_chatgpt: {e}")
            