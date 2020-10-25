from lacmusDB.db_definition import Image, create_file_entity

class Processing():
    @staticmethod
    def process_incoming_file(path:str):
        # check file in valid image
        # if not - move to errors
        # if yes - upload to s3, create record in DB, delete, create label in in_process
        new_image = Image(filename=path)
        create_file_entity(new_image)
        return