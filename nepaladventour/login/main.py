from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle

app = FastAPI()

# Define your data model for inputs using Pydantic
class UserPreferences(BaseModel):
    preferences: dict  # Adjust based on your model's input

# Load your model
with open('Model\AI\Hotel_Recommender.ipynb', 'rb') as model_file:
    model = pickle.load(model_file)

@app.post('/recommendations/')
async def get_recommendations(user_prefs: UserPreferences):
    try:
        # Assuming your model's predict method can handle dictionary inputs
        recommendations = model.predict(user_prefs.preferences)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)