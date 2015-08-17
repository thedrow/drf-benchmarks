#!/usr/bin/env python
# coding: utf-8
import pkgutil

serializers_to_test = []
nested_serializers_to_test = []
serializer_ids = []
nested_serializer_ids = []
for importer, modname, ispkg in pkgutil.walk_packages(__path__, __package__ + '.'):
    if ispkg:
        try:
            module = importer.find_module(modname).load_module(modname)
        except (ImportError, AttributeError):
            pass
        else:
            try:
                serializer_id = modname.rsplit('.', 1)[1].replace('_', ' ').capitalize() + ' '
                serializers_to_test.append(module.TestSerializer)
                serializer_ids.append(serializer_id)

                nested_serializers_to_test.append(module.TestNestedSerializer)
                nested_serializer_ids.append(serializer_id)
            except AttributeError:
                pass

assert serializers_to_test, "No serializers could not be loaded."
