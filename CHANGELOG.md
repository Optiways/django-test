==========
Change Log
==========


# [0.0.2] - 2022-09-13

Changed
-------

* Override get_form to hide other bus_stop and bus_shift instances
* Override get_queryset to hide user non authorized instances
* Add filter factory for BusStop and Driver models in filters.py
* Add initialization script to accelerate db reset

Fixed
-------
* Fix time_stop validators by changing filters parameters
* Fix undefined travel_time value by using CharField instead of TimeField format (temporary)

# [0.0.1] - 2022-09-09

Changed
-------

* Implement Django BusStop ModelForm
* Delete Django BusShift ModelForm


# [0.0.0] - 2022-09-07

Changed
-------

* Add Validators
* Add Django BusShift ModelForm
* Add Django Models
* Add readme file
* Add gitignore file
* Add requirements file
