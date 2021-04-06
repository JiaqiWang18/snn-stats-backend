from server import ma, models


class UnitedStatesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.UnitedStates


class CaliforniaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.California


class LACountySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.LACounty


class OrangeCountySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.OrangeCounty


class OCCitiesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = models.OCCities
