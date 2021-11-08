"""
Creates JSON source files for opentabulate according to a variable map csv.

File organization:
    dir/
        json/ # output folder for src files.
        variablemap.csv
        jsongenerator.py
"""

import csv


def main():
    ccFields = ['name', 'source_id', 'source_facility_type', 'full_address',
                'capacity', 'licence_status', 'facility_type', 'ages',
                'infant', 'toddler', 'school_age', 'phone', 'email', 'contact']
    addressFields = ['municipality', 'prov/terr', 'latitude', 'longitude', 'geometry']
    # forceFields = ['format','data_provider']
    input_file = csv.DictReader(open('variablemap.csv'))

    for row in input_file:
        OP = open("json/" + row['prov/terr'].lower().replace(' ', '-')
                            + "-childare-src" + ".json","w")

        # General information -----
        OP.write('{ \n')
        OP.write('    "localfile": "' + row['file_name'] + '.' + row['format'] + '",\n')
        OP.write('    "schema_groups": ' + '["childcare", "address"],\n')
        OP.write('    "source": "' + row['source_url'] + '",\n')
        OP.write('    "licence": "' + row['licence'] + '",\n')
        OP.write('    "provider": "' + row['data_provider'] + '",\n')

        if row['format'] == "csv":
            OP.write('    "format": {\n         "type": "' + row['format']  + '",\n'
                                    + '         "delimiter": ",",\n'
                                    + '         "quote": "\\""'
                                    + '\n},\n')

        elif row['format'] == "shp":
            OP.write('    "format": {\n         "type": "' + row['format'] + '"\n},\n')

        first = True
        other = False
        # force = False

        OP.write('    "schema": {\n')
        # Childcare fields ------
        OP.write('        "childcare": {\n')
        for f in ccFields:
            if row[f] != '':
                if first:
                    first = False
                else:
                    OP.write(',\n')
                OP.write('        "'+ f +'": "' + row[f] + '"')
                other = True

        OP.write('  \n}')

        if not first:
            OP.write(',\n')
        add = False

        # Address fields --------
        for f in addressFields:
            if row[f] != '':
                add = True
        if add:
            # if other or force:
                # OP.write(',\n')
            OP.write('         "address": {\n')
            first = True

            for f in addressFields:
                if row[f] != '':
                    if first:
                        first = False
                    else:
                        OP.write(',\n')
                    OP.write('            "'+ f + '": "' + row[f] + '"')
            OP.write('\n        }\n')
        OP.write('    }\n')

        OP.write('}')
        OP.close()

if __name__ == "__main__":
    main()
