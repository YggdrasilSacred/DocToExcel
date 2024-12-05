from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# Store connection information
endpoint = "https://docintfeng.cognitiveservices.azure.com/"
key = "2Z8HNY6b1GBW09PuvORQr8Gh5jGZVSLKdKqasgcVTCvvq8laThXKJQQJ99ALACYeBjFXJ3w3AAALACOGzNgZ"

fileUri = "https://github.com/MicrosoftLearning/mslearn-ai-document-intelligence/blob/main/Labfiles/01-prebuild-models/test-invoices/iCuci_Apr_23.pdf?raw=true"
fileLocale = "en-US"
fileModelId = "prebuilt-invoice"

print(f"\nConnecting to Forms Recognizer at: {endpoint}")
print(f"Analyzing invoice at: {fileUri}")

# Create the client

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Analyse the invoice

poller = document_analysis_client.begin_analyze_document_from_url(
    fileModelId, fileUri, locale=fileLocale 
)
invoices = poller.result()

# Display invoice information to the user

for idx, invoice in enumerate(invoices.documents):
    print("--------Recognizing invoice #{}--------".format(idx + 1))
    
    ### ----Invoice header details---- ###

    # Invoice number
    invoice_number = invoice.fields.get("InvoiceId")
    if invoice_number:
        print(
            "Invoice Number: {} has confidence: {}".format(
                invoice_number.value, invoice_number.confidence
            )
        )

    # Invoice date
    invoice_date = invoice.fields.get("InvoiceDate")
    if invoice_date:
        print(
            "Invoice Date: {} has confidence: {}".format(
                invoice_date.value, invoice_date.confidence
            )
        )

    ### ----Billing Information---- ###

    # Bill Recipient
    billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
    if billing_address_recipient:
        print(
            "Billing Address Recipient: {} has confidence: {}".format(
                billing_address_recipient.value,
                billing_address_recipient.confidence,
            )
        )

    ### ----Service/Item Details---- ###

    print("Invoice items:")

    for idx, item in enumerate(invoice.fields.get("Items").value):
        print("...Item #{}".format(idx + 1))

        # Description
        item_description = item.value.get("Description")    
        if item_description:
            print(
                "......Description: {} has confidence: {}".format(
                    item_description.value, item_description.confidence
                )
            )

        # Item total amount
        amount = item.value.get("Amount")
        if amount:
            print(
                "......Amount: {} has confidence: {}".format(
                    amount.value, amount.confidence
                )
            )

    print("----------------------------------------")

print("\nAnalysis complete.\n")