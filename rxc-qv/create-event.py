import csv, re, requests, json, time, sys, getopt

def main(argv):
    outputfile = 'events.csv'
    dev = False
    port = '2000'
    try:
        opts, args = getopt.getopt(argv,"hdp:o:",["dev", "port=", "ofile="])
        input_file = args[0]
        csvfile = open(input_file, newline='')
        reader = csv.reader(csvfile)
    except:
        print('create-event.py -d -p <port> -o <outputfile> <input_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('create-event.py -d -p <port> -o <outputfile> <input_file>')
            sys.exit()
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-d", "--dev"):
            dev = True
        elif opt in ("-p", "--port"):
            port = arg

    # skip headers
    next(reader)
    next(reader)
    proposals = []
    for row in reader:
        proposal = {
            "title": row[0] + ' -- ' + row[3],
            "description": "",
            "url": row[2],
        }
        proposal["description"] += '1st Chamber Sponsor(s): ' + ', '.join(row[4].split()) + '\n'
        proposal["description"] += '2nd Chamber Sponsor(s): ' + ', '.join(row[5].split()) + '\n'
        proposal["description"] += '\nFY22-23\n'
        proposal["description"] += 'Revenue: ' + row[6] + '\n'
        proposal["description"] += 'Expenditures: ' + row[7] + '\n'
        proposal["description"] += 'Transfers: ' + row[8] + '\n'
        proposal["description"] += 'Net Budget Impact: ' + row[9] + '\n'
        proposal["description"] += '\nFY23-24\n'
        proposal["description"] += 'Revenue: ' + row[10] + '\n'
        proposal["description"] += 'Expenditures: ' + row[11] + '\n'
        proposal["description"] += 'Transfers: ' + row[12] + '\n'
        proposal["description"] += 'Net Budget Impact: ' + row[13] + '\n'

        proposals.append(proposal)
    proposals.sort(key=lambda p: p['title'].split(' -- ')[1])

    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "event_title": "Ongoing General Fund Prioritization [test]",
        "event_description": "",
        "num_voters": 10,
        "credits_per_voter": 100,
        "start_event_date": "2022-04-04T20:55:52.057Z",
        "end_event_date": "2022-04-20T20:55:52.057Z",
        "subjects": proposals,
    }
    url = 'https://colorado.qv.radicalxchange.org' if not dev else 'http://localhost:' + port
    r = requests.post(
        url + '/api/events/create',
        headers=headers,
        data=json.dumps(data)
    )
    if r.status_code != 200:
        print(r.raise_for_status())
        sys.exit(2)
    else:
        print("Event created successfully.")

    response_data = r.json()

    with open(outputfile, 'a') as out:
        out.write(url + '/event?id=' + response_data["id"] + '&secret=' + response_data["secret_key"] + '\n')

if __name__ == "__main__":
    main(sys.argv[1:])
