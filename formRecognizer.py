#import credentials from config file
import config
#import azure from recognizer libraries
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError
# create client and authenticate with the endpoint and key
endpoint = config.endpoint
key = config.key
#create client and authenticate with the endpoint and key

form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
form_training_client = FormTrainingClient(endpoint, AzureKeyCredential(key))

myReceiptUrl = "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/master/sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/receipt/contoso-receipt.png"

#user form recognizer client to recognize image from myReceiptUrl
poller = form_recognizer_client.begin_recognize_receipts_from_url(myReceiptUrl)
result = poller.result()

#loop through results and extract data from receipt
for receipt in result:
    for name, field in receipt.fields.items():
        # each field is of type FormField
        # label_data is populated if you are using a model trained without labels,
        # since the service needs to make predictions for labels if not explicitly given to it.
        if name == "MerchantName":
            if field.value:
                print("Merchant Name: {} has confidence: {}".format(field.value, field.confidence))
            elif field.label_data:
                print("Merchant Name: {} has confidence: {}".format(field.label_data.text, field.confidence))

        if name == "TransactionDate":
            if field.value:
                print("Transaction Date: {} has confidence: {}".format(field.value, field.confidence))
            elif field.label_data:
                print("Transaction Date: {} has confidence: {}".format(field.label_data.text, field.confidence))

        if name == "Items":
            if field.value:
                print("Receipt Items:")
                for idx, item in enumerate(field.value):
                    print("...Item #{}".format(idx+1))
                    item_name = item.value.get("Name")
                    item_quantity = item.value.get("Quantity")
                    item_price = item.value.get("Price")
                    item_total_price = item.value.get("TotalPrice")
                    if item_name:
                        print("......Item Name: {} has confidence: {}".format(item_name.value, item_name.confidence))
                    if item_quantity:
                        print("......Item Quantity: {} has confidence: {}".format(item_quantity.value, item_quantity.confidence))
                    if item_price:
                        print("......Individual Item Price: {} has confidence: {}".format(item_price.value, item_price.confidence))
                    if item_total_price:
                        print("......Total Item Price: {} has confidence: {}".format(item_total_price.value, item_total_price.confidence))
            elif field.label_data:
                print("Receipt Items:")
                for idx, item in enumerate(field.value):
                    print("...Item #{}".format(idx+1))
                    item_name = item.value.get("Name")
                    item_quantity = item.value.get("Quantity")
                    item_price = item.value.get("Price")
                    item_total_price = item.value.get("TotalPrice")
                    if item_name:
                        print("......Item Name: {} has confidence: {}".format(item_name.label_data.text, item_name.confidence))
                    if item_quantity:
                        print("......Item Quantity: {} has confidence: {}".format(item_quantity.label))