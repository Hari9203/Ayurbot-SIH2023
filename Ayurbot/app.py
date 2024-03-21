from flask import Flask, render_template, request, jsonify
import random
import cv2
import numpy as np
from keras.models import load_model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return chat_with_bot(input.lower())

user_responses={}
capture=[]
myprak=['recommendation']
scale={
        'height': ['short', 'medium', 'tall'],
        'weight': ['light', 'average', 'heavy'],
        'skin type': ['dry', 'warm','oily'],
        'age': ['0-100'],
        'voice_tone': ['weak', 'strong','deep']
    }

patterns = {
    'name': ['I am a chatbot.\nI go by the name Ayurbot.'],
    'hello': ['Hello! How can I assist you?', 'Hi there! What can I do for you?', 'Hey! How may I help you?'],
    'hey': ['Hello! What can I do for you?', 'Hi there! How can I assist you?', 'Hey! How may I help you?'],
    'hi': ['Hello! What can I do for you?', 'Hey! How can I assist you? How may I help you?'],
    'prak': ["Of course! To determine your Prakruti type,\nI'll need to ask you a few questions\nAre you ready to get started?"],
    'recommendation': ["Tell me your prakriti type"],
    'pit': ["Raw Salads, cooked grains, milk, seeds are the best foods\nto maintain health without any vitamin deficiency. Hot,\nSpicy foods should be avoided.\nPitta individuals are prone to digestive issues,skin\nproblems, inflammation, and stress-related conditions\ndue to their fiery and intense nature.\nWould you like more detailed recommendations for diet\nand lifestyle based on your Prakruti?"],
    'vat': ["Favor naturally sweet foods like fruits, most grains,\nroot vegetables, milk, ghee, fresh yogurt, eggs, nuts,\nseeds, oils, and lean meats.\nVata individuals are prone to diseases like anxiety,\ninsomnia, digestive issues, arthritis, and nervous system\ndisorders.\nWould you like more detailed recommendations for diet\nand lifestyle based on your Prakruti?"],
    'kap': ["Warm, light, and dry food is favorable, or cooked light\nmeals. Kaphas do best with lightly cooked foods or\nraw fruits and vegetables.\nKapha-dominant individuals are prone to conditions\nlike obesity, respiratory issues, congestion, and\nsluggish metabolism.\nWould you like more detailed\nrecommendations for diet and lifestyle based on\nyour Prakruti?"],
    'sure': ["Great! I'll provide you with a customized plan based on\nyour Prakruti type.\nPlease provide your email address, and I'll send it to you."],
    '@': ["You'll receive your personalized Ayurvedic\nrecommendations in your email shortly.\nIf you have any more questions or need further assistance,\nfeel free to ask."],
    'link':["https://shorturl.at/fgoFX"],
    'nearby':["Can I have access to your locations"],
    'access':["1. Ayurveda center (3 km)\n2.Senji Ayurveda clinic   (4.2 km)"],
    'thank': ["Thank you, hope it was helpful"],
    'bye': ['Until we meet again, goodbye!', 'See you later!', 'Have a great day!','Goodbye for now! Stay safe and be well....'],
}

def classify_prakriti(user_responses):
    vata_score = 0
    pitta_score = 0
    kapha_score = 0

    height = user_responses['height']
    weight = user_responses['weight']
    skin_type = user_responses['skin']
    age = user_responses['age']
    voice_tone = user_responses['voice']

    if "tall" in height:
        vata_score += 1 
    elif "medium" in height:
        pitta_score += 1
    else:
        kapha_score += 1
    
    if int(age) < 30:
        kapha_score += 1 
    elif int(age) < 50:
        pitta_score += 1  
    else:
        vata_score +=1
    
    if "light" in weight:
        vata_score += 1 
    elif "average" in weight:
        pitta_score += 1 
    else:
        kapha_score += 1
    
    if "dry" in skin_type:
        vata_score += 1 
    elif "warm" in skin_type:
        pitta_score += 1 
    else:
        kapha_score += 1
    
    if "weak" in voice_tone:
        vata_score += 1 
    elif "strong" in voice_tone:
        kapha_score +=1 
    else:
        pitta_score +=1

    if vata_score > pitta_score and vata_score > kapha_score:
        return "Vata."
    elif pitta_score > vata_score and pitta_score > kapha_score:
        return "Pitta."
    else:
        return "Kapha."


def chat_with_bot(user_input):
    face_analysis = False
    response = None
    if True:

        if user_input == 'quit':
            response = 'Goodbye for now! Stay safe and be well.'

        elif 'ready' in user_input or 'option' in user_input or 'start' in user_input or 'yes' in user_input:
            response = "Do you want to analyze using\n1. face or\n 2. Provide 'height', 'age', 'weight', 'skin type', and 'voice_type'? or\n 3. Using BMI"
            
        elif "2" in user_input and 'go' in user_input:
            ch="height"
            temp=''
            for k in scale[ch]:
                temp=temp+k+", "
            response="Please provide your "+ ch + " on the scale "+ temp
            
        elif 'height' in user_input:
            x=list(map(str,user_input.split()))
            for feature in x:
                if feature in 'shortmediumtall':
                    user_responses['height']=feature
                    break
            ch='weight'
            temp=''
            for k in scale[ch]:
                temp=temp+k+", "
            response="Please provide your "+ ch + " on the scale "+ temp
            
        elif 'weight' in user_input:
            x=list(map(str,user_input.split()))
            for feature in x:
                if feature in 'lightaverageheavy':
                    user_responses['weight']=feature
                    break
            ch='skin type'
            temp=''
            for k in scale[ch]:
                temp=temp+k+", "
            response="Please provide your "+ ch + " on the scale "+ temp
            
        elif 'skin' in user_input:
            x=list(map(str,user_input.split()))
            for feature in x:
                if feature in 'drywarmoily':
                    user_responses['skin']=feature
                    break
            ch='age'
            temp=''
            for k in scale[ch]:
                temp=temp+k+", "
            response="Please provide your "+ ch + " on the scale "+ temp
            
        elif 'age' in user_input:
            x=list(map(str,user_input.split()))
            for feature in x:
                if feature.isdigit():
                    user_responses['age']=feature
                    break
            ch='voice_tone'
            temp=''
            for k in scale[ch]:
                temp=temp+k+", "
            response="Please provide your "+ ch + " on the scale "+ temp
            
        elif 'voice' in user_input or 'tone' in user_input:
            x=list(map(str,user_input.split()))
            for feature in x:
                if feature in 'weakstrongdeep':
                    user_responses['voice']=feature
                    break

            classification_result = classify_prakriti(user_responses)
            myprak.append(classification_result)
            response='Your Prakriti type is '+ classification_result
            return response
                   
        elif '3' in user_input or 'kg' in user_input or 'cm' in user_input or 'bmi' in user_input:
            if '3' in user_input or 'bmi' in user_input and 'kg' not in user_input and 'cm' not in user_input:
                response="Give me your weight in kgs"
            elif 'kg' in user_input:
                response="Give me your height in cms"
                x=list(map(str,user_input.split()))
                for feature in x:
                    if feature.isdigit():
                        capture.append(feature)
                        break   
            elif 'cm' in user_input:
                x=list(map(str,user_input.split()))
                for feature in x:
                    if feature.isdigit():
                        capture.append(feature)
                        break
                def calculate_BMI(weight_kg, height_m):
                    bmi = weight_kg / (height_m ** 2)
                    if bmi < 18.5:
                        return "Vata"
                    elif 18.5 <= bmi< 25.0:
                        return "Pitta"
                    else:
                        return "Kapha"
                    
                d=calculate_BMI(int(capture[0]),int(capture[1])/100)
                myprak.append(str(d))
                response='Your prakriti type is '+str(d)
           
        elif "1" in user_input or "face" in user_input:

            np.set_printoptions(suppress=True)

            model = load_model("keras_Model.h5", compile=False)
            class_names = open("labels.txt", "r").readlines()

            camera = cv2.VideoCapture(0)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            confidence=[]
            while True:

                ret, frame = camera.read()

                desired_size = (224, 224)

                resized_frame = cv2.resize(frame, desired_size, interpolation=cv2.INTER_AREA)

                image = np.asarray(resized_frame, dtype=np.float32).reshape(1, desired_size[1], desired_size[0], 3)
                image = (image / 127.5) - 1

                prediction = model.predict(image)
                index = np.argmax(prediction)
                class_name = class_names[index]
                confidence_score = prediction[0][index]

                faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                cv2.putText(frame, 'Prakriti Type: ' + class_name[2:], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, 'Confidence Score: ' + str(np.round(confidence_score * 100))[:-2] + '%', (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                cv2.imshow("Webcam Image", frame)
                conf=str(np.round(confidence_score * 100))[:-2]
                confidence.append(conf)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            camera.release()
            cv2.destroyAllWindows()
            myprak.append(class_name[2:])
            response="Your Prakriti type is "+ class_name[2:] +"Confidence Score: "+ str(max(confidence)) + '%'
            
     
        else:
            if "recommend" in user_input:
                for pattern, responses in patterns.items():
                    if pattern in myprak[-1].lower():
                        response = '' + random.choice(responses)
                        return response
                
            for pattern, responses in patterns.items():
                if pattern in user_input.lower():
                    response = '' + random.choice(responses)
                    break
                else:
                    response="Enter a valid prompt"

    return response

if __name__ == '__main__':
    app.run()
