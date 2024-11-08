from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.collections import InstrumentedList
from .fields import File
from sqlalchemy.orm.attributes import get_history

class TableFieldCheck:
    __common_fields = [
        'registry', 'metadata', 'create',
        "bulk_create", "update", "bulk_update",
        "delete", "bulk_delete", "save"
    ]

    def _is_table_field(self, field):
        return not field.startswith("_") and field not in self.__common_fields and getattr(self, field).__class__ != InstrumentedList

class HandleRemoveFile:
    def _file_remove_handle(self, data):
        for key, value in data.items():
            attr = getattr(self.__table__.c, key)
            attr.remove(value)

class FieldValidation(TableFieldCheck):
    
    @property
    def _validate(self):
        data = []
        all_fields = self.__dir__()
        
        for field in all_fields:
            if self._is_table_field(field):
                attr = getattr(self.__table__.c, field)
                if not getattr(attr, "primary_key") and not getattr(attr, "default") and not getattr(attr, "nullable") and not getattr(self, attr.key):
                    data.append({attr.key:"This value is not be empty"})

        return data
    
    @property
    async def _file_upload_handle(self):
        data = {}
        all_fields = self.__dir__()
        error = []
        for field in all_fields:
            if self._is_table_field(field):
                attr = getattr(self.__table__.c, field)
                file_data = getattr(self, field)
                
                if (attr.__class__ == File) and file_data:
                    data[field] = await attr.upload(file=file_data)
                    if not data[field]:
                        error.append({field:"Error to upload file"})
                    else:
                        setattr(self, field, data[field])

        return error, data

class UpdateMethodRemoveFile:
    def _update_method_remove_file_get(self):
        all_fields = self.__dir__()
        data = {}
        for field in all_fields:
            if self._is_table_field(field):
                attr = getattr(self.__table__.c, field)
                file_data = getattr(self, field)

                if (attr.__class__ == File) and file_data:
                    x = get_history(self, field)
                    if x.deleted:
                        data[field] = x.deleted[0]
        
        return data

class DeleteMethodRemoveFile(TableFieldCheck, HandleRemoveFile):
    def _delete_method_remove_file_get(self):
        data = {}
        all_fields = self.__dir__()
        for field in all_fields:
            if self._is_table_field(field):
                attr = getattr(self.__table__.c, field)
                if (attr.__class__ == File):
                    file_data = getattr(self, field)
                    data[field] = file_data
                    
        return self._file_remove_handle(data)


# MODELS CRUD MIXIN #
class CreateMixin(FieldValidation, HandleRemoveFile):

    async def create(self, session, refresh=True):
        error = self._validate
        if error:return False, error

        error, data = await self._file_upload_handle
        if error:
            self._file_remove_handle(data)
            return False, error
        
        try:
            session.add(self)
            session.commit()

            if refresh:
                session.refresh(self)
            return True, self
        except (SQLAlchemyError, IntegrityError, Exception) as e:
            session.rollback()
            self._file_remove_handle(data)
            return False, [str(e)]
        
    async def bulk_create(self, session, data:list=[]):
        if not data:
            return False, ["Data is not found!"]
        try:
            stmt = insert(self.__class__).values(data)
            result = session.execute(stmt)
            session.commit()
        except (SQLAlchemyError, IntegrityError, Exception) as e:
            session.rollback()
            return False, str(e)
        session.close()
        return True, result.lastrowid

class UpdateMixin(FieldValidation, UpdateMethodRemoveFile, HandleRemoveFile):
    async def update(self, session, refresh=True):
        try:
            
            error = self._validate

            if error:
                session.close()
                return False, error
            
            error, data = await self._file_upload_handle

            print(data)

            if error:
                self._file_remove_handle(data)
                return False, error
            
            old_data = self._update_method_remove_file_get()
            session.commit()
            if refresh:
                session.refresh(self)
            
            session.close()
            self._file_remove_handle(old_data)
            return True, self
        
        except (SQLAlchemyError, IntegrityError, Exception) as e:
            self._file_remove_handle(data)
            session.rollback()
            return False, [str(e)]

    async def bulk_update(self, session, data:list=[]):
        if not data:
            return False, ["Data is not found!"]
        
        try:
            session.bulk_update_mappings(self.__class__, data)
            session.commit()
            return True, [i["id"] for i in data]
        except (SQLAlchemyError, IntegrityError, Exception) as e:
            session.rollback()
            return False, str(e)
        
class DeleteMixin(DeleteMethodRemoveFile):
    async def delete(self, session):
        try:
            self._delete_method_remove_file_get()
            session.delete(self)
            session.commit()
            session.close()
            return True, None
        
        except (SQLAlchemyError, IntegrityError, Exception) as e:
            session.rollback()
            session.close()
            return False, str(e)
        
    async def bulk_delete(self, session, data:list=[]):
        if not data:
            return False, "Data is not found!"
        
        session.query(self.__class__).filter(
            self.__class__.id.in_(data)
        ).delete(synchronize_session=False)
        
        session.commit()
        session.close()
        return await self.delete(session, data)

