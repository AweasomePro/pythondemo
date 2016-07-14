define({ "api": [
  {
    "type": "post",
    "url": "/product/hoousepackage/?action=create",
    "title": "",
    "name": "create_new_hotel_package",
    "group": "partner_____",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "hotelid",
            "optional": false,
            "field": "id",
            "description": "<p>of hte hotel model primary key.</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "firstname",
            "description": "<p>Firstname of the User.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "lastname",
            "description": "<p>Lastname of the User.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "hotelBooking/views/product/housepackage.py",
    "groupTitle": "partner_____"
  }
] });
