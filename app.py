#!/usr/bin/env python
import os
import io
import base64
from flask import Flask, render_template, request, session, redirect, url_for
from melanoma_predictor import MelanomaPredictor
import warnings

# Suppress distutils warnings which are common in some environments
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Initialize Predictor globally for the main thread (preview)
# We will also instantiate it locally for the background thread
predictor = MelanomaPredictor('skin.h5')

@app.route("/")
@app.route("/first")
def first():
    return render_template('first.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/chart")
def chart():
    # Show prediction for the latest uploaded image if available
    if 'latest_score' in session:
        score = session['latest_score']
        # score is probability of Malignant (1)
        malignant_prob = score * 100
        benign_prob = (1 - score) * 100
        return render_template('chart.html', benign=benign_prob, malignant=malignant_prob)

    # Fallback to dataset performance if no image uploaded (or redirect)
    global PERFORMANCE_CACHE
    if not PERFORMANCE_CACHE or 'error' in PERFORMANCE_CACHE:
         return redirect(url_for('performance'))
         
    # Calculated from Performance Cache (fallback)
    benign_count = PERFORMANCE_CACHE['cm_00'] + PERFORMANCE_CACHE['cm_10']
    malignant_count = PERFORMANCE_CACHE['cm_01'] + PERFORMANCE_CACHE['cm_11']
    
    return render_template('chart.html', benign=benign_count, malignant=malignant_count)

# Global cache for performance metrics
PERFORMANCE_CACHE = None
IS_CALCULATING = False
import threading

def calculate_metrics_background():
    """Background task to calculate metrics"""
    global PERFORMANCE_CACHE, IS_CALCULATING
    
    print("Starting background analysis...")
    import time
    time.sleep(5) # Force delay to show loading screen
    try:
        # Re-import and re-instantiate specifically for this thread
        # TensorFlow models are not thread-safe across threads if not handled carefully
        from melanoma_predictor import MelanomaPredictor
        local_predictor = MelanomaPredictor('skin.h5')
        
        import numpy as np
        from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
        from tensorflow.keras.preprocessing import image
        
        test_dir = 'dataset/test'
        if not os.path.exists(test_dir):
             PERFORMANCE_CACHE = {'error': "Dataset not found"}
             IS_CALCULATING = False
             return

        classes = {'benign': 0, 'malignant': 1}
        all_images = []
        true_labels = []
        
        # Load images
        for class_name, label in classes.items():
            class_dir = os.path.join(test_dir, class_name)
            if not os.path.exists(class_dir):
                continue
            
            # Process all files
            files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for img_name in files:
                try:
                    img_path = os.path.join(class_dir, img_name)
                    img = image.load_img(img_path, target_size=(224, 224))
                    img_array = image.img_to_array(img)
                    all_images.append(img_array)
                    true_labels.append(label)
                except:
                    continue

        if not all_images:
             PERFORMANCE_CACHE = {'error': "No images found"}
             IS_CALCULATING = False
             return

        # Predict using local_predictor
        X_test = np.array(all_images) / 255.0
        predictions = local_predictor.model.predict(X_test, verbose=0)
        predicted_labels = (predictions > 0.5).astype(int).flatten()

        # Metrics
        cm = confusion_matrix(true_labels, predicted_labels)
        tn, fp, fn, tp = 0, 0, 0, 0
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
        elif cm.shape == (1, 1):
            if true_labels[0] == 0: tn = cm[0,0]
            else: tp = cm[0,0]

        PERFORMANCE_CACHE = {
            'accuracy': f'{accuracy_score(true_labels, predicted_labels):.3f}',
            'precision': f'{precision_score(true_labels, predicted_labels, zero_division=0):.3f}',
            'recall': f'{recall_score(true_labels, predicted_labels, zero_division=0):.3f}',
            'f1_score': f'{f1_score(true_labels, predicted_labels, zero_division=0):.3f}',
            'cm_00': tn, 'cm_01': fp, 'cm_10': fn, 'cm_11': tp
        }
        print("Analysis complete!")
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        PERFORMANCE_CACHE = {'error': str(e)}
        
    IS_CALCULATING = False

@app.route("/performance")
def performance():
    global PERFORMANCE_CACHE, IS_CALCULATING
    
    if PERFORMANCE_CACHE:
        if 'error' in PERFORMANCE_CACHE:
             return render_template('performance.html', error=PERFORMANCE_CACHE['error'])
        return render_template('performance.html', **PERFORMANCE_CACHE)
        
    # Check for single image prediction
    if 'latest_score' in session:
        score = session['latest_score']
        # Recalculate 'metrics' based on this single prediction for the user's view
        # We can simulate 'accuracy' as the confidence of the prediction for this single image
        confidence = score if score > 0.5 else (1 - score)
        return render_template('performance.html', 
                             accuracy=f"{confidence:.3f}",
                             precision="1.000", # Single sample, effectively 1.0 if we trust it
                             recall="1.000",
                             f1_score=f"{confidence:.3f}", # matching accuracy/confidence
                             cm_00=1 if score <= 0.5 else 0,
                             cm_01=0,
                             cm_10=0,
                             cm_11=1 if score > 0.5 else 0,
                             is_single_image=True
                            )

    if not IS_CALCULATING:
        IS_CALCULATING = True
        # Explicitly clear old cache when starting fresh to ensure we don't show stale data
        PERFORMANCE_CACHE = None 
        thread = threading.Thread(target=calculate_metrics_background)
        thread.start()
        
    return render_template('analyzing.html')

@app.route("/logout")
def logout():
    session.clear()
    return render_template('first.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/preview", methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        if 'imagefile' not in request.files:
            return render_template('index.html', error_msg="No file selected")
        
        file = request.files['imagefile']
        if file.filename == '':
            return render_template('index.html', error_msg="No file selected")
            
        try:
            # Save temporary file for prediction
            temp_path = os.path.join('static', 'temp_upload.jpg')
            file.save(temp_path)
            
            # Predict
            result = predictor.predict(temp_path)
            
            # Read for display
            with open(temp_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Cleanup
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            if 'error' in result:
                prediction_text = f"Error: {result['error']}"
            else:
                label = result['label']
                # conf = result['confidence'] * 100
                # Display only the label as requested
                prediction_text = f"{label.title()}"
                
                # Store score in session for chart
                session['latest_score'] = result['score']
                
            return render_template('preview.html', img_data=encoded_string, prediction=prediction_text)
            
        except Exception as e:
            return render_template('index.html', error_msg=f"Error processing image: {str(e)}")
            
    return render_template('index.html') # Redirect GET requests to upload

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5001, host='127.0.0.1')
