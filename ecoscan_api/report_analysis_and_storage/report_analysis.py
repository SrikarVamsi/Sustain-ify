from fastapi import APIRouter, Depends, status, HTTPException, Body, File, UploadFile

from .firebase_helper import uploadFileToFireBase, pushDataToRealtimeFBDB, getUrlsOfUser

from .prompts import extract_details_from_report

from wrapper import typeDocInputNOutputFormat, model

from .output_strucutre import ReportContent

from generate_random_id import generate_unique_code



router = APIRouter(
    prefix="/report-storage",
    tags=['Report-Analysis and Storage']
)


@router.get('/test')
def testRouter():
    return {"success": "Work's Like a Charm"}

@router.post('/analyse-and-upload')
async def analyseAndUploadReport(userId: str, fileInput: UploadFile = File(...)):
    # try:
    # process inputs
    user_id = userId
    file_binary_content = await fileInput.read()
    file_type = fileInput.content_type
    _, file_extension = fileInput.filename.split('.')

    # store the file temp to give gemini input
    file_path = 'media/reports/temp.{}'.format(file_extension)

    with open(file_path, 'wb') as jammer:
        jammer.write(file_binary_content)

    # load to gemini storage for generation and get response about the pdf and type
    response = eval(typeDocInputNOutputFormat(model, extract_details_from_report, ReportContent, file_path)) # a dict of values

    # upload file to firebase media manager
    # uploadFileToFireBase()
    report_categorized_type = response['report_type']

    cloud_path = F"{userId}/{report_categorized_type}/{generate_unique_code()}.{file_extension}"

    with open(file_path, 'rb') as jammer:
        uploadFileToFireBase(jammer.read(), file_type, cloud_path)

    # upload doc details to FireBase RealtimeDB
    final_data_push = {
        'user-id': user_id,
        'report-category': report_categorized_type,
        'report-cloud-path': cloud_path,
        'report-content': response['report_content']
    }

    # pushing the data successfully
    pushDataToRealtimeFBDB(final_data_push)

    # return {"Upload": "Successful :))"}
    return final_data_push

    # except:
    #     raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Something went wrong, check userId or the file accepted.")


@router.post('/fetch-user-reports-url')
def fetchUrlsOfUserReportsAndTypes(usedId: str):
    try:
        return getUrlsOfUser(usedId)
    except:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not Found!!!")




# @router.post('/just-upload')
# def justUpload():
#     return