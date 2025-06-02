User Manual

  Introductory Manual
    The following are the steps the user must take to use the system:
      1. Install Requirements
        o npm install express axios cors
        o pip install flask joblib numpy pandas
      2. Run Servers
        o node nodeToFlask.js
        o py flaskserver.py
      3.	Open the Tool
        o	Visit the website: jeremynilsen.com/tbu/hash.html
      4.	Choose a Model (Optional)
        o	There will be a dropdown menu with different selectable AI models.  These models correlate with the different machine learning algorithms used in training.  If ignored, it defaults to Random Forest.
      5.	Paste Your Hashes
        o	In the textbox, paste the hash or hashes to be identified.  If multiple hashes are inputted, they must be separated into one hash per line.
      6.	Submit Your Input
        o	Click the “Submit” button below the textbox
      7.	View Results
        o	The results will be generated into a table below the “Submit” button
        
  System Reference Manual
    Listing of Services:
      •	Algorithm Prediction
        o	  For every given hash digest, the tool processes the user’s input and provides a prediction for which cryptographic hashing algorithm was most likely used in its generation.  
            The prediction is displayed next to the corresponding input hash.
      •	Model Selection
        o	  Users may optionally select from a selection of available AI models via a dropdown menu.  These models differ based on the machine learning algorithm used for training each checkpoint.
      Error Recovery:
        •	Incorrect Input
            o	If the user enters an unexpected or invalid input, i.e. something that is not a valid hash such as random words or incomplete hashes, the system will provide 
            unexpected and invalid predictions.  To recover, replace the inputs in the textbox with valid inputs and click the “Submit” button again. 
        •	System Fails to Respond
            o	If the page stops responding or no predictions are returned, the user can recover by simply refreshing the page.

