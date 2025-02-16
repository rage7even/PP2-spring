import json

with open('D:\PP2spring\py lab 4\sample-data.json', 'r') as json_file:
    data = json.load(json_file)

    print("Interface Status")
    print("=" * 80)
    print("{:<50} {:<20} {:<7} {:<6}". format("DN", "Description", "Speed", "MTU"))
    print("-" * 80)

    for item in data['imdata']:
        attributes = item['l1PhysIf']['attributes']
        dn = attributes['dn']
        descr = attributes.get('descr', '')
        speed = attributes.get('speed', 'N/A')
        mtu = attributes.get('mtu', 'N/A')

        print("{:<50} {:<20} {:<7} {:<6}".format(dn,descr,speed,mtu))