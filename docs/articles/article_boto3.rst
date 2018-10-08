===========================
Getting started with Boto 3
===========================

.. _Boto 3 Documentation: https://boto3.readthedocs.io

Presentation
============

Quoting the `Boto 3 Documentation`_:
Boto is the Amazon Web Services (AWS) SDK for Python, which allows Python developers to write software
that makes use of Amazon services like S3 and EC2. Boto provides an easy to use, object-oriented API
as well as low-level direct service access.


Configuration
=============

To use Boto 3, you should set up authentication credentials.

You can create the credential files in your home directory. Its location is ``~/.aws/credentials:``:

.. code-block:: ini

    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_KEY

And set the region in ``~/.aws/config``:

.. code-block:: ini

    [default]
    region=us-east-1

This sets up credentials for the default profile as well as a default region to use when creating connections.


Using Amazon Glacier
====================

.. _Boto 3 Docs - Glacier: https://boto3.readthedocs.io/en/latest/reference/services/glacier.html

In the context of the archiving workflow, we use the **Glacier** service (but not the **S3**).

The documentation of the Glacier service is available in the `Boto 3 Docs - Glacier`_


List the vaults
---------------

To list the vaults, you can do:

>>> import boto3

>>> glacier = boto3.resource('glacier')
>>> for vault in glacier.vaults.all():
...     print(vault)
...
glacier.Vault(account_id=u'-', name=u'201407')
glacier.Vault(account_id=u'-', name=u'201408')
glacier.Vault(account_id=u'-', name=u'201409')
glacier.Vault(account_id=u'-', name=u'201410')
glacier.Vault(account_id=u'-', name=u'201411')
glacier.Vault(account_id=u'-', name=u'201412')
glacier.Vault(account_id=u'-', name=u'201501')
glacier.Vault(account_id=u'-', name=u'201502')
glacier.Vault(account_id=u'-', name=u'201503')
glacier.Vault(account_id=u'-', name=u'201504')
glacier.Vault(account_id=u'-', name=u'201505')
glacier.Vault(account_id=u'-', name=u'201506')
glacier.Vault(account_id=u'-', name=u'201507')
glacier.Vault(account_id=u'-', name=u'201508')
glacier.Vault(account_id=u'-', name=u'201509')
glacier.Vault(account_id=u'-', name=u'201510')
glacier.Vault(account_id=u'-', name=u'201511')
glacier.Vault(account_id=u'-', name=u'201512')
glacier.Vault(account_id=u'-', name=u'201601')
glacier.Vault(account_id=u'-', name=u'201602')
glacier.Vault(account_id=u'-', name=u'201603')
glacier.Vault(account_id=u'-', name=u'201604')
glacier.Vault(account_id=u'-', name=u'201605')
glacier.Vault(account_id=u'-', name=u'201606')
glacier.Vault(account_id=u'-', name=u'201607')
glacier.Vault(account_id=u'-', name=u'201608')
glacier.Vault(account_id=u'-', name=u'Archivage_Cloud')
glacier.Vault(account_id=u'-', name=u'archivage-test')


Read the vault attributes
-------------------------

To read the attributes of a vault:

>>> vault = glacier.Vault(account_id=u'-', name='201407')

>>> vault.creation_date
u'2014-07-30T15:34:14.204Z'

>>> vault.last_inventory_date
u'2014-08-01T14:30:07.697Z'

>>> vault.number_of_archives
28

>>> vault.size_in_bytes
311490089

>>> vault.vault_arn
u'arn:aws:glacier:us-east-1:033342878933:vaults/201407'

>>> vault.vault_name
'201407'


Create a new vault
------------------

To create a new vault:

>>> vault = glacier.create_vault(vaultName="test-201610")
>>> vault
glacier.Vault(account_id=u'-', name='test-201610')

Or:

>>> vault = glacier.Vault('-', 'test-201611')
>>> vault.create()


Delete an empty vault
---------------------

To delete an empty vault:

>>> vault = glacier.Vault(account_id=u'-', name='test-201610')
>>> vault.delete()

If the vault is not empty, you'll get an exception:

>>> glacier.Vault(account_id=u'-', name='archivage-test').delete()
Traceback (most recent call last):
  ...
botocore.exceptions.ClientError: An error occurred (InvalidParameterValueException) when calling \
the DeleteVault operation: Vault not empty or recently written to: \
arn:aws:glacier:us-east-1:033342878933:vaults/archivage-test


List the archives (inventory)
-----------------------------

To list the archives stored in a vault, you can do:

>>> vault = glacier.Vault("-", "201407")

➢ Initiate vault inventory:

>>> job = vault.initiate_inventory_retrieval()
>>> job
glacier.Job(account_id='-', vault_name='201407',
            id='m-DLDuNO52qrwBiZuPPedUk0j5kuD8vXywiZAuNKOj6V1Khn_8pQcpQLNks9B5qgDwnap_iE0gDVuoBjAoalPSMmxgt8')

**Wait at least 4 hours...**

➢ To get information about an initiated job:

>>> import pprint

>>> client = boto3.client("glacier")

On a pending job:

>>> pprint.pprint(client.describe_job(vaultName="201407", jobId=job.id))
{u'Action': u'InventoryRetrieval',
 u'Completed': False,
 u'CreationDate': u'2016-09-01T09:16:45.612Z',
 u'InventoryRetrievalParameters': {u'Format': u'JSON'},
 u'JobId': u'm-DLDuNO52qrwBiZuPPedUk0j5kuD8vXywiZAuNKOj6V1Khn_8pQcpQLNks9B5qgDwnap_iE0gDVuoBjAoalPSMmxgt8',
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '623',
                                      'content-type': 'application/json',
                                      'date': 'Thu, 01 Sep 2016 09:41:32 GMT',
                                      'x-amzn-requestid': 'J9msS0OWqVlxdZWHRoh1k2cpZg39pUUjvjLXjD0SCoZM6N4'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'J9msS0OWqVlxdZWHRoh1k2cpZg39pUUjvjLXjD0SCoZM6N4'},
 u'StatusCode': u'InProgress',
 u'VaultARN': u'arn:aws:glacier:us-east-1:033342878933:vaults/201407'}

On a completed job:

>>> pprint.pprint(client.describe_job(vaultName="201407", jobId=job.id))
{u'Action': u'InventoryRetrieval',
 u'Completed': True,
 u'CompletionDate': u'2016-09-01T13:15:48.835Z',
 u'CreationDate': u'2016-09-01T09:16:45.612Z',
 u'InventoryRetrievalParameters': {u'Format': u'JSON'},
 u'InventorySizeInBytes': 9011,
 u'JobId': u'm-DLDuNO52qrwBiZuPPedUk0j5kuD8vXywiZAuNKOj6V1Khn_8pQcpQLNks9B5qgDwnap_iE0gDVuoBjAoalPSMmxgt8',
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '650',
                                      'content-type': 'application/json',
                                      'date': 'Thu, 01 Sep 2016 13:38:24 GMT',
                                      'x-amzn-requestid': 'Rh7kT9rgw7LbuAMK3j50ffpsQ-TN0836_oau2aVODuo6QcM'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'Rh7kT9rgw7LbuAMK3j50ffpsQ-TN0836_oau2aVODuo6QcM'},
 u'StatusCode': u'Succeeded',
 u'StatusMessage': u'Succeeded',
 u'VaultARN': u'arn:aws:glacier:us-east-1:033342878933:vaults/201407'}


➢ To list the current jobs for a vault:

>>> pprint.pprint(client.list_jobs(vaultName="201407"))
{u'JobList': [{u'Action': u'InventoryRetrieval',
               u'Completed': False,
               u'CreationDate': u'2016-09-01T09:16:45.612Z',
               u'InventoryRetrievalParameters': {u'Format': u'JSON'},
               u'JobId': u'm-DLDuNO52qrwBiZuPPedUk0j5kuD8vXywiZAuNKOj6V1Khn_8pQcpQLNks9B5qgDwnap_iE0gDVuoBjAoalPSMmxgt8',
               u'StatusCode': u'InProgress',
               u'VaultARN': u'arn:aws:glacier:us-east-1:033342878933:vaults/201407'}],
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '651',
                                      'content-type': 'application/json',
                                      'date': 'Thu, 01 Sep 2016 09:51:44 GMT',
                                      'x-amzn-requestid': 'r7Yf_JWvED327F-5N0a5gv_191wWIih0cfGhXIxhbshjP2k'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'r7Yf_JWvED327F-5N0a5gv_191wWIih0cfGhXIxhbshjP2k'}}


➢ To download a job output:

* If your job is not completed:

>>> job.get_output()
Traceback (most recent call last):
  ...
botocore.exceptions.ClientError: An error occurred (InvalidParameterValueException) when calling \
the GetJobOutput operation: The job is not currently available for download: \
m-DLDuNO52qrwBiZuPPedUk0j5kuD8vXywiZAuNKOj6V1Khn_8pQcpQLNks9B5qgDwnap_iE0gDVuoBjAoalPSMmxgt8

* If your job is completed:

>>> response = job.get_output()

By default the inventory list is returned as a JSON body.


>>> pprint.pprint(response)
{'ResponseMetadata': {'HTTPHeaders': {'accept-ranges': 'bytes',
                                      'content-length': '9011',
                                      'content-type': 'application/json',
                                      'date': 'Thu, 01 Sep 2016 13:42:41 GMT',
                                      'x-amzn-requestid': 'o8YRRnkj9FrrLAIOzUrLL9cRarNadmIXc1WPHUy4tBsJ9ho'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'o8YRRnkj9FrrLAIOzUrLL9cRarNadmIXc1WPHUy4tBsJ9ho'},
 u'acceptRanges': 'bytes',
 u'body': <botocore.response.StreamingBody object at 0x1a37950>,
 u'contentType': 'application/json',
 u'status': 200}

The Content-Type is ``application/json``, so, to get the inventory:

>>> import json

>>> inventory = json.load(response["body"])

>>> pprint.pprint(inventory)
{u'ArchiveList': [{u'ArchiveDescription': u'',
                   u'ArchiveId': u'TliOiBR45aBgpBm-YXqTYCI51c_lcS0yjBoTS-7QrSCJmcZTyfVU1AyiOY2jtD2-P8YbuEXzkSGPq9sT9maCHZVSbNgn581PaAMFQu41p9n8b5nS9sqQKj1nxF58WgZwt1_5RxaEhg',
                   u'CreationDate': u'2014-07-30T15:34:15Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'vr7J3baZqNDufzeSYZm4EtP3Ouk6HDLL3-HAdSOul-p-kId-IPHjyp7M-uPZJnTx4hPjKQp00t2Lkk4l6JoFlxlTxapxcdTufllFttzyKYXTm5SWUMb9C06e9pJV0vkWfGl6FL9IYg',
                   u'CreationDate': u'2014-07-30T15:37:27Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'Ahm87egVaRu6M86TdbfDlamFxAN7OFSgkLdNcqQLDDHKIWY7vX5gO-_tui1sgE_VBkXm8CjQKL5wbzSi6UO2VL1hJzRlZ6F2PadJ1S89sVFpuIqhEDXxpwt7Tdeyk6EFweg6us8jnw',
                   u'CreationDate': u'2014-07-30T15:40:07Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'yoNTc3V_E_83FTNXdntiiaJoQH-JRlH-3Jgm0RNrMXPXRAMxw1_KB47wDGnG0nDJz8obUjS-2h818VFk_KWtJ7-YleDYt1-2t1sQlifFqAv3DXnT5TfwYmgdIw107NFroRYtZ5yCcw',
                   u'CreationDate': u'2014-07-30T15:40:44Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'vdPtNLg8kyTH7hWsHcBCazt76ISTFkSNU0j1f9Vxfzn3-ps4MyhY4jmSI5K50Og7llwYakp5fXLK3ove-2GFpdvMSZMGz3Dn7VX9slXRhYuWaGHNYYaW8H0PfZfaLzK_9VK_xkJ4Yw',
                   u'CreationDate': u'2014-07-30T15:43:41Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'j9iPZTq8b35uuMoKxkvEwH6jOWpB6WosrTjH-kXUevRpGgGDiBuz7JpROSx6XkkbIxkHLrb5bk4DixTDFLBDesmwFdGgxa38Dbak-1Z8ZweBoVMjV7XerYZAdWfvknQ1maU5lsYR_Q',
                   u'CreationDate': u'2014-07-30T15:45:15Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'nleCzqbI3BWMH9ar97I77Rj3QxC2Dpj4ErrsvYZ0kMhf9z7fG7YpsfsqeU6gN_LyEX8y7-gAUpPjqC6Ev2EJt-Kkcnz7Ayq5Ha6-Ce35h7aneMNF_flu7qgXCFlN92_4asrXCzc5ZQ',
                   u'CreationDate': u'2014-07-30T15:47:57Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'/jcrtra/archivage/traitement/tmp/99999991.ok.checksum',
                   u'ArchiveId': u'CnWsDxY6YmjmIIjkKYKPh3TTRsnok1dDR9ZZj9rTryXVbtVMxRseLXETzm3B4BG7ZbCHoPenkjg-tX-OoasVMxVbW9J6BD54ZlmV2dokHJMHdpA6RfzRt5VoBnZYCmwxkoGmQqEBRQ',
                   u'CreationDate': u'2014-07-30T15:53:06Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'F-uMiX5ipSxryN5FMa46zQ8KH2IZPmeZEa1zqRy2Yt_dVB9Y84m-vvfElDReg1pOWxLXjVJK98neoqDhNXA4tnBx7_XaqkbtnaHNLR5hFSn_KgBM8Y5TsUXQ4o5QJ605XW2sarSJDg',
                   u'CreationDate': u'2014-07-30T15:53:51Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'6EVIbFcFIjxOYeRKGoRfr5eInbQiu5GwAG99KglWz1DevxKy8DY2HMvQAT4mvHBu1Aq7YCfalVp8zA3KSguK7Ly9On6LByp5Ehl9AKSh2zhuZpu_TiZBLTQVzUhCODSjvw86CQ-ZrQ',
                   u'CreationDate': u'2014-07-30T15:55:45Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'pQ-fc_cSgMtK6ytDRYkE0kKXpmN6towkLKZbuCLFr9V8I3tIN2i-oGGz0XtAfUMsAXpO95ElCleaJetI4Apu-Nb3qiva_UhkZPOBnFsmghP0LP1FBPkXgrE3AUzZADhMB4oDGfnZ9w',
                   u'CreationDate': u'2014-07-30T15:56:11Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'KKB6c76XFFX9UItRnBVdmsvVcKRtFMm_lLDT3g0dCNp_9zZlNdZR4Hh8KkTWgbmHxTCpLDxmLr2CLx02A3zITk5zcr0Fi0ZbMn7ULF7kG5apNX1m7ZtC-7SscXfXjQMfI0e0Dfy5UQ',
                   u'CreationDate': u'2014-07-30T15:59:35Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'ypZYe-Wl1A39HmV0l1Rvkj56MStB8ohDZ5RjtOZyxZBsM4iQbCYYKjeYDtNF3kt-7q-VTRoA99_iwZgQI4vZ98SseyvbTuf0j4ZqVjDvl7z-FZnf6iKuWyNQz-yiVnnZNybnlNNwew',
                   u'CreationDate': u'2014-07-30T16:00:23Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'RESULT',
                   u'ArchiveId': u'smO4CbU_N3TE_j5yh0AXVtMeoiqyMypImZEJAMDb1adkfMntVHK5qYEjdkNJWSIJOjsOl4rIqJFGhGHz85Mp7OyvwHJ_DNczXxtYp62DIEhmQxFtzx3MWMutQtI5vjkHcoot3UOc5Q',
                   u'CreationDate': u'2014-07-31T09:16:55Z',
                   u'SHA256TreeHash': u'01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
                   u'Size': 1},
                  {u'ArchiveDescription': u'RESULT',
                   u'ArchiveId': u'woDx6QJYc5rQSgsUL9YcpMdXMjK-3WQJ9ToAvgpvhwfhTG4fMeJRMPUXW5sGl-NJKe-l23q3hY81BOA9GCfXnjaLgnEtCr0vsnye3DyvpV6iS4ZaT7GvRyOADWMd6tTufyq4-76T7A',
                   u'CreationDate': u'2014-07-31T09:33:03Z',
                   u'SHA256TreeHash': u'01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
                   u'Size': 1},
                  {u'ArchiveDescription': u'RESULT',
                   u'ArchiveId': u'_BlyqsOGvNPjTXRiMa8fruzl_HHRp6lJad_KPGA3b4vEm8MyzymAwsR4lsH0QZq--13aOCJlknI6_UWguFbs0GA6JxDzptIX0RqKXLS-KwMhAEwCE23jyegargNO2x_T2BtP7Ddm2A',
                   u'CreationDate': u'2014-07-31T09:44:00Z',
                   u'SHA256TreeHash': u'01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
                   u'Size': 1},
                  {u'ArchiveDescription': u'RESULT',
                   u'ArchiveId': u'q4qW-wtiOdZXDnpLaLDSvgODp69kpmi8u3QBV1tNU4Cj7gKi2jj4jnVAdSqoNUX5S2kzirWCEET5VXQ7iC8ijR-SBcf-QByNtFcJj8JH3CHDD8ejclYvhpagBhcwfoiPXZ1ksppKWw',
                   u'CreationDate': u'2014-07-31T09:44:55Z',
                   u'SHA256TreeHash': u'01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
                   u'Size': 1},
                  {u'ArchiveDescription': u'RESULT',
                   u'ArchiveId': u'snqZ0rleoi9uQMhWq-UcitA9tQBKTDq7RLP_IeHA9FyK5B4lfPYW2_AyItjNWtYlNZ3LVGsbvVOHsVpJTU7dz1PVX9FVmRkWXpARMzTaQeoROXSZdrUR_ppurFLqKFYsaUp9ADIdFg',
                   u'CreationDate': u'2014-07-31T09:45:40Z',
                   u'SHA256TreeHash': u'01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b',
                   u'Size': 1},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'3lIWPB08rS12FS13oZgIEdaEF2F8KYtmNvFTUWLO_5NLgMuQ5SOhYVF6UHCM2ihjrQ-5wIiOpEOsDumiZbr-eHSSQoEZiNNPZS-Yqn7AgUD73Tt2qSPNc9zOwnzrJ2b_TS-rBS7FHQ',
                   u'CreationDate': u'2014-07-31T12:33:50Z',
                   u'SHA256TreeHash': u'7214bedef670c311afc1242e5feddb09d4b940b201576a192626bee57e256f3a',
                   u'Size': 200},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'vpaaevdhxHPgIYK9a6MuYbuoo5g1qWJ9c5MbFJfdiohNELua_tcbOMnfwd2lkQAX90I9Xfti214RrQvcBa8rxB-gyEURAx0wl_MfPJu_aARzkDnig6WkOiC64dZlHFyeQRiD4Vvi6g',
                   u'CreationDate': u'2014-07-31T12:36:10Z',
                   u'SHA256TreeHash': u'ac7de61d6dcf6a17e53981fc934b2ff0637a05326a4107471c6d86757f5ee55a',
                   u'Size': 217},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'sCzpAtDbm4E8YjFyYbEZJecKTOpZD1IvtzmL2aLny3DjPVHy6maYX0N9gmaJcBrqG-yk-lkvau-2W2YPTW5Kh6j-J_gjuVnj1yrUSUbVpmFJft9jKOJBfRQNsHFRaJIEquI58VinbQ',
                   u'CreationDate': u'2014-07-31T13:02:41Z',
                   u'SHA256TreeHash': u'59bfdd7eca767778ae79cc41be6ecc45ad969c87c02afdf95a1b42a20f67fc8f',
                   u'Size': 195},
                  {u'ArchiveDescription': u'ar.txt',
                   u'ArchiveId': u'7mbgi9tH6hs_bPHXTZXWF11F16Ew7wGiHyLmlE6vvV307Fs8Z7g7Ze9E6q3aM2hSK9B98lmfrivZTYlUvCAMbOXvR6nhKcUMhbLv7HguAkAaVUYGEGCuz4yMIm03AzPuNX0vMR78-g',
                   u'CreationDate': u'2014-07-31T13:26:55Z',
                   u'SHA256TreeHash': u'ad24f6d0197057374526ea99beef5c099287667a930a84df3715298d23fa3e78',
                   u'Size': 62},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'AWPPUj_I79TgXiW351HmkLTTZfXFcNt8OltqTRzvIdjBcLxUtHGBisPzfQDiMd1-ujenUcBIKZ0g9gXM8NEr1UL4Lg3dmHpt_6GQ8q88PGGiJajPuHH2d5-wy3W-hdRGNT-Wabmdrw',
                   u'CreationDate': u'2014-07-31T15:19:01Z',
                   u'SHA256TreeHash': u'6d97f0399218712bb2a545daf3668ff80b58b02d9acc639b528bbeb34f9d5171',
                   u'Size': 87226186},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'jp-mwgd-j_FiBVMo9_K2W1AIx21x86cqKfMOxVqiI6k_9RmCdMVarr3WRufS0wkw7LQxWZhJGXhbTgFt6fLdSm3J-yyxhxQUX_HtRjkzeIGYjU6JRhT4WZr8TkL3kxALeqZQ00Rwzg',
                   u'CreationDate': u'2014-07-31T15:45:08Z',
                   u'SHA256TreeHash': u'83ce82671e7157354230ce72c3b182ec3c906ca856108cb7b035d71fc84ce7c8',
                   u'Size': 94786093},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'i_mViix-T3dTJDi59zMftZzqyxU2kVBNwGmUwk6GjpV38Rym2nB7iLJAfh3gbaXna12PvOqb96LeCjrdvKQe0RpNO3Xb8RsBvTVj2YvSM9LcGpBMYBxCJKIxX6jx4fxeqYvsCM_naQ',
                   u'CreationDate': u'2014-07-31T15:58:55Z',
                   u'SHA256TreeHash': u'b06228db50d176226c444ea801d894082666286bbafdbae85cd9d85ae32d9c6b',
                   u'Size': 91765322},
                  {u'ArchiveDescription': u'',
                   u'ArchiveId': u'jYHe3odau2xwjdirD7CLk8nMiTU79NKpPq0mBbDLRS49lO27ZYextSKvTXeULHhwHC8IPWBvcagu29r1NgoqdNYyH_1m-x12y7vTfq3MgdyCspEJZ4qv3k-CJZVAmtQvUGT6-Jq3-g',
                   u'CreationDate': u'2014-07-31T16:08:25Z',
                   u'SHA256TreeHash': u'd3989acb87b806146702bdd1a96076d6ae8bfb14819547c9d33012f1e61f0748',
                   u'Size': 36790798},
                  {u'ArchiveDescription': u'TEST-AR_18_10_2013.log',
                   u'ArchiveId': u'bZPFp4S1Cz-B8uIB4FtGs63eia9uOlhN7nm9H96YNtErb5N28UfCZmPPUoI6BtCC80YxQJ6EUExGZcd6eLQS5GS-8O9cTOH8W65s7psEqSTfGYDpybUUIWx_A-5OYo1LdqfnQKSIgQ',
                   u'CreationDate': u'2014-08-01T07:52:40Z',
                   u'SHA256TreeHash': u'17857f630ab0704ad0e185d8864d23903c4134c9d04505ea899f9ea2db9e5bb1',
                   u'Size': 343},
                  {u'ArchiveDescription': u'TEST-AR_18_10_2013_cheminfull.log',
                   u'ArchiveId': u'waVwXa3jgzAERIghV17zM4rlqVjArVH_rm9I67UZDbBYxWlGIrMuE31yrX534IhgzX7iH-XiUVgpOCRKmY7cw0Yl1-Lq5eUSlRkymIuDrG8vGecMuNs_qeTHKqBgpRX2Pv4IishPfQ',
                   u'CreationDate': u'2014-08-01T07:54:08Z',
                   u'SHA256TreeHash': u'17857f630ab0704ad0e185d8864d23903c4134c9d04505ea899f9ea2db9e5bb1',
                   u'Size': 343}],
 u'InventoryDate': u'2014-08-01T14:30:07Z',
 u'VaultARN': u'arn:aws:glacier:us-east-1:033342878933:vaults/201407'}


Upload an archive
-----------------

First, create an archive:

>>> import os, shutil
>>>
>>> base_name = os.path.abspath(".")
>>> base_name
'/DATA_raid/llaporte/workspace/my_archive'

>>> arch_path = shutil.make_archive(base_name, "zip")
>>> arch_path
'/DATA_raid/llaporte/workspace/my_archive.zip'

To upload an archive, open the file in binary mode:

>>> import io
>>>
>>> with io.open(arch_path, mode="rb") as fd:
...     archive = vault.upload_archive(archiveDescription="Was in: " + arch_path, body=fd)
...

You get the archive instance with a archive ID.

>>> archive
glacier.Archive(account_id='-',
vault_name='test-201609',
id='_V2e8LSh0nHhgaRslckF2Sxs4C22Bjw7Q05DIa4X_4V5LcanzfG3O5LnWiKGMPehK_Wi-7q0gLZ_pTn3XzijFW2aHWSVtBJpKmEhuFanZCsVhwFtys6dP-zFlKVh0PxLhbx8m_THmw')


Delete an archive
-----------------

To delete an archive:

>>> archive = glacier.Archive(account_id='-',
... vault_name='test-201609',
... id='_V2e8LSh0nHhgaRslckF2Sxs4C22Bjw7Q05DIa4X_4V5LcanzfG3O5LnWiKGMPehK_Wi-7q0gLZ_pTn3XzijFW2aHWSVtBJpKmEhuFanZCsVhwFtys6dP-zFlKVh0PxLhbx8m_THmw')

>>> archive.delete()


Download an archive (retrieval)
-------------------------------

This operation initiates a job to retrieve an archive.

>>> job = archive.initiate_archive_retrieval()

**Wait at least 4 hours...**

➢ To get information about an initiated job:

On a pending job:

>>> pprint.pprint(client.describe_job(vaultName=vault.vault_name, jobId=job.id))
{u'Action': u'ArchiveRetrieval',
 u'ArchiveId': u'TgCPA9cpYEGWVo6-_TDVqkHeeA7g_6opDeu2KZv_6GVf98sOWqwyVca5sxOmz6k--yegDNONmbO-iR-hnMbgeESA5T6w_Fs2N11YoqgX7FW-Rtovl3KXkbwUjrTTj9bQUlFVN1LlXw',
 u'ArchiveSHA256TreeHash': u'983707d8d4bd9527c538ceee061cae3bd5a6306d7700306271c8e8b9a963c460',
 u'ArchiveSizeInBytes': 2132743,
 u'Completed': False,
 u'CreationDate': u'2016-09-01T15:03:48.365Z',
 u'JobId': u'vJo5-KLs3G5-JgWSw2IQAmbC4qKaOVtlXwUBdBDLhcQA1bNT7z0_RnffszPmpEGq8ErWuM_PWB8yK9wBTQsQOyzJokNW',
 'ResponseMetadata': {'HTTPHeaders': {'content-length': '824',
                                      'content-type': 'application/json',
                                      'date': 'Thu, 01 Sep 2016 15:04:18 GMT',
                                      'x-amzn-requestid': 'jyJ7IqXP8SDZ9wxYMa21vhfZ_F-0WjTZN-m-Y_UR2Pqjgyc'},
                      'HTTPStatusCode': 200,
                      'RequestId': 'jyJ7IqXP8SDZ9wxYMa21vhfZ_F-0WjTZN-m-Y_UR2Pqjgyc'},
 u'RetrievalByteRange': u'0-2132742',
 u'SHA256TreeHash': u'983707d8d4bd9527c538ceee061cae3bd5a6306d7700306271c8e8b9a963c460',
 u'StatusCode': u'InProgress',
 u'VaultARN': u'arn:aws:glacier:us-east-1:033342878933:vaults/test-201609'}

➢ To download a job output:

* If your job is not completed:

>>> job.get_output()
Traceback (most recent call last):
  ...
botocore.exceptions.ClientError: An error occurred (InvalidParameterValueException) when calling \
the GetJobOutput operation: The job is not currently available for download: \
vJo5-KLs3G5-JgWSw2IQAmbC4qKaOVtlXwUBdBDLhcQA1bNT7z0_RnffszPmpEGq8ErWuM_PWB8yK9wBTQsQOyzJokNW

* If your job is completed:

>>> response = job.get_output()

By default the inventory list is returned as the following JSON body.

