import asyncio
import os

import pymongo
import yaml

from data.ExtractionData import ExtractionData
from data.ExtractionMessage import ExtractionMessage
from data.Task import Task
from information_extraction.InformationExtraction import InformationExtraction
from rsmq import RedisSMQ

from tasks.Tasks import Tasks

ROOT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DOCKER_VOLUME = f'{ROOT_DIRECTORY}/docker_volume'


def get_paths(tenant: str, pdf_file_name: str):
    file_name = ''.join(pdf_file_name.split('.')[:-1])
    pdf_file_path = f'{DOCKER_VOLUME}/to_extract/{tenant}/{pdf_file_name}'
    xml_file_path = f'{DOCKER_VOLUME}/xml/{tenant}/{file_name}.xml'
    failed_pdf_path = f'{DOCKER_VOLUME}/failed_pdf/{tenant}/{pdf_file_name}'
    return pdf_file_path, xml_file_path, failed_pdf_path


def extract_paragraphs() -> ExtractionMessage:
    client = pymongo.MongoClient('mongodb://mongo_paragraphs:27017')

    task = Tasks.get_next_task()

    if not task:
        return

    pdf_file_path, xml_file_path, failed_pdf_path = get_paths(task.tenant, task.pdf_file_name)
    information_extraction = InformationExtraction.from_pdf_path(pdf_path=pdf_file_path,
                                                                 xml_file_path=xml_file_path,
                                                                 failed_pdf_path=failed_pdf_path)

    if not information_extraction:
        return ExtractionMessage(tenant=task.tenant,
                                 pdf_file_name=task.pdf_file_name,
                                 success=False)

    extraction_data = ExtractionData.from_segments(tenant=task.tenant,
                                                   pdf_file_name=task.pdf_file_name,
                                                   segments=information_extraction.segments)

    client['pdf_paragraph'].paragraphs.insert_one(extraction_data.dict())
    os.remove(pdf_file_path)

    return ExtractionMessage(tenant=task.tenant,
                             pdf_file_name=task.pdf_file_name,
                             success=True)


async def extract_paragraphs_async(redis_server: str):
    extraction_message = extract_paragraphs()
    # if extraction_message:
    #     queue = RedisSMQ(host=redis_server, qname="paragraphs_extraction")
    #     queue.sendMessage(delay=0).message(extraction_message.json()).execute()
    await asyncio.sleep(1)


def loop_extract_paragraphs():
    if os.path.exists('redis_server.yml'):
        redis_server = yaml.safe_load(open("redis_server.yml", 'r'))['redis_server']
    else:
        redis_server = 'redis_paragraphs'

    while True:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(extract_paragraphs_async(redis_server))


if __name__ == '__main__':
    loop_extract_paragraphs()