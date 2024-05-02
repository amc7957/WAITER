def speech_to_text():
 
    import speech_recognition as sr
    from speech_recognition.recognizers import google, whisper
    import pyttsx3 
 
    # use sr recognizer 
    r = sr.Recognizer() 
     
    while(1):    

        try:
         
        # initialize microphone
            with sr.Microphone() as microphone:
             
                # wait for ambient noise level to be adjusted
                r.adjust_for_ambient_noise(microphone, duration=0.2)
             
                # listen for speech
                microphone = r.listen(microphone)
             
                # use google recognizer to figure out what
                #was said
                MyText = r.recognize_google(microphone)
                MyText = MyText.lower()
 
                return(MyText)
             
        except sr.RequestError as e:
            print("Error; {0}".format(e))
            break
         
        except sr.UnknownValueError:
            print("Error")
            break