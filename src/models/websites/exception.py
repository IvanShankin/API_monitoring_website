from src.models.base.exception import NoDataForUpdate, NotFoundData


class WebsiteNotFound(NotFoundData):
    pass


class NoDataForUpdateWebsite(NoDataForUpdate):
    pass