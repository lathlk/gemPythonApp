from bottle import Bottle, run, get, post, request, response, static_file
import label_image as li
import zipfile
import os

'''
    Instructions
    1. Train the model and get the retrained_graph.pb and the label file to the scripts directory inside model folder
    2. Copy the image and put it into inference_image folder
    3. Call the get_labels function in the label_image script

    Note: Make sure you have installed tensorflow or run it in the anaconda
'''

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

html = '''
    <html>
        <head>
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        </head>
        <body class="card card-body" >
            <div class="jumbotron text-center"
                <h6><span class="badge badge-secondary">More than a GEM Detector</span></h6>
                <h1 class="display-4">Gem stones identifier <span style="font-size:30px; color:gray">with machine learning and Image procesing</span></h1>
                <p class="lead">Make the final decision by considering the Gem Master system to predict the type of the Gem</p>
                <hr class="my-4">
                <form method="post" action="{0}" enctype="multipart/form-data">
                    <input type="file" name="{1}" class="btn btn-lg"/>
                    <input class="btn btn-success btn-lg" type="submit" value="{2}" />
                </form>
                <hr class="my-4">
                <p>A gemstone is one of most valuable and precious stone what we can take from ground. According to the definition of Cambridge dictionary gem is a precious stone especially when cut into a regular shape. There are some countries which are treasure lands for some of most wonderful varieties of gemstones on earth. Colombia, Africa, Madagascar, Sri Lanka, Myanmar and Australia are the biggest producers of some of the most eye catching and enthralling stones in the world. Most importantly gemstones are taken for jewelries. Rather than the mineral stones certain rocks such as lapis, lazuli and opal and some organic materials such as amber jet and pearl are also used in jewelries. Gemstones can be categorized in to two main categories, such as precious stones and semiprecious stones Quantitative grading of gemstones is a challenging task even for skilled gem assessors. Current gemstones evaluation practices are highly subjective due to the complexities of gemstones assessment and the limitations of human visual observation. In this paper, we present a novel machine vision system for identify the major features of a gemstone, the Gem Master. The proposing solution is based on statistical machine learning and image processing with multiple characteristics extracted from gemstones' images. The assessment workflow includes image enhancement, image analysis, and gemstones classification, finding cracks and identifying the cutting shapes of gemstones.</p>               
            </div>
            <div class="row">
                <div class="col-lg-3 col-md-3 col-sm-6">
                    <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ51Q6GfFhnUJD9dpaOohn8gTXh01kbR7tqtsfshtTU9XvAhZ7t&s" class="card-img-top" alt="...">
                    </div>
                </div>
                <div class="col-lg-3 col-md-3 col-sm-6">
                    <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                        <img src="https://cdn.shopify.com/s/files/1/0380/5717/products/pear-chatham-lab-grown-blue-sapphire-gems_1800x1800.png?v=1535067510" class="card-img-top" alt="...">
                    </div>
                </div>
                <div class="col-lg-3 col-md-3 col-sm-6">
                    <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWpaIEBJd9ySYIglLBvC5pfFK-S2vEKK0fqkdOtIVHQb-IDZ5gqA&s" class="card-img-top" alt="...">
                    </div>
                </div>
                <div class="col-lg-3 col-md-3 col-sm-6">
                    <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpmSBrFgNBKE04pyIoEf4emny2RJQNbCuzJi2FhmaLMqKvonFa&s" class="card-img-top" alt="...">
                    </div>
                </div>
            </div>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
        </body>
    </html>
'''
# Hooks
app = Bottle()
@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

# pages

# @get('/')
@app.route('/', method=['OPTIONS', 'GET'])
def indexPage():
    return html.format("/upload", "image", "Predict")

# @get('/upload-model')
@app.route('/upload-model', method=['OPTIONS', 'GET'])
def uploadModelPage():
    return html.format("/upload-model", "model", "Upload Model")

# other routes

# File to change


# @post('/upload')
@app.route('/upload', method=['OPTIONS', 'POST'])
def uploadImage():
    image = request.files.image
    filename = "inference_image/image.jpg"
    _openAndSaveFile(filename, image)
    
    imagefile = static_file('image.jpg', root=dir_path+'/'+'inference_image/')
    prediction = _getTopPredictions()
    page = '''
        <html>
            <head>
                <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
            </head>
            <body class="card card-body" >
                <div class="jumbotron text-center">
                    <h6><span class="badge badge-secondary">More than a GEM Detector</span></h6>
                    <h1 class="display-4">Gem stones identifier <span style="font-size:30px; color:gray">with machine learning and Image procesing</span></h1>
                    <p class="lead">Make the final decision by considering the Gem Master system to predict the type of the Gem</p>
                    <hr class="my-4">
                    <div class="row">
                        <div class="col-md-6 col-lg-6">
                            <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                                <img src="{1}" class="card-img-top" alt="...">
                            </div>
                        </div>
                        <div class="col-md-6 col-lg-6">
                            <h1>This is a <span style="color:red;">{0}</h1>
                        </div>
                    </div>
                    <hr class="my-4">
                    <p>A gemstone is one of most valuable and precious stone what we can take from ground. According to the definition of Cambridge dictionary gem is a precious stone especially when cut into a regular shape. There are some countries which are treasure lands for some of most wonderful varieties of gemstones on earth. Colombia, Africa, Madagascar, Sri Lanka, Myanmar and Australia are the biggest producers of some of the most eye catching and enthralling stones in the world. Most importantly gemstones are taken for jewelries. Rather than the mineral stones certain rocks such as lapis, lazuli and opal and some organic materials such as amber jet and pearl are also used in jewelries. Gemstones can be categorized in to two main categories, such as precious stones and semiprecious stones Quantitative grading of gemstones is a challenging task even for skilled gem assessors. Current gemstones evaluation practices are highly subjective due to the complexities of gemstones assessment and the limitations of human visual observation. In this paper, we present a novel machine vision system for identify the major features of a gemstone, the Gem Master. The proposing solution is based on statistical machine learning and image processing with multiple characteristics extracted from gemstones' images. The assessment workflow includes image enhancement, image analysis, and gemstones classification, finding cracks and identifying the cutting shapes of gemstones.</p>               
                </div>
                <div class="row">
                    <div class="col-lg-3 col-md-3 col-sm-6">
                        <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ51Q6GfFhnUJD9dpaOohn8gTXh01kbR7tqtsfshtTU9XvAhZ7t&s" class="card-img-top" alt="...">
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-6">
                        <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                            <img src="https://cdn.shopify.com/s/files/1/0380/5717/products/pear-chatham-lab-grown-blue-sapphire-gems_1800x1800.png?v=1535067510" class="card-img-top" alt="...">
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-6">
                        <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWpaIEBJd9ySYIglLBvC5pfFK-S2vEKK0fqkdOtIVHQb-IDZ5gqA&s" class="card-img-top" alt="...">
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-6">
                        <div class="card" style="width: 18rem;margin: 0 auto;float:none;">
                            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpmSBrFgNBKE04pyIoEf4emny2RJQNbCuzJi2FhmaLMqKvonFa&s" class="card-img-top" alt="...">
                        </div>
                    </div>
                </div>
                <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
            </body>
        </html>
    '''

    return page.format(prediction, imagefile)




# @get('/predictions')
@app.route('/predictions', method=['OPTIONS', 'GET'])
def get_prediction():
    prediction = _getTopPredictions()
    page = """
        <html>
            <body>
                <h1>{0}</h1>
            </body>
        </html>
    """

    return page.format(prediction)


# @post('/upload-model')
@app.route('/upload-model', method=['OPTIONS', 'POST'])
def uploadsModel():
    modelZip = request.files.model
    filename = "model/model.zip"
    _openAndSaveFile(filename, modelZip)

    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall("model/")
    zip_ref.close()

# Utility functions

def _getTopPredictions():
    lable_index, labels_list, results_list = li.get_lables("image.jpg")
    best_guess = ""
    guess_percentage = 0
    for i in lable_index:
        if guess_percentage < float(results_list[i]):
            best_guess = labels_list[i]
            guess_percentage = float(results_list[i])
    """
    print("best guess ", best_guess)
    print("lable_index  ", lable_index)
    print("labels_list ", labels_list)
    print("results_list guess ", results_list)

    selected_list = [{"class": labels_list[i], "probability": float(results_list[i]) } for i in lable_index]
    """
    return best_guess

def _openAndSaveFile(filename, uploadedFile):
    with open(filename,'wb') as open_file:
        open_file.write(uploadedFile.file.read())
    open_file.close()


#run(reloader=True,debug=True)
run(app, host='0.0.0.0', port=os.environ.get('PORT', '5000'))
