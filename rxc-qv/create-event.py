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

    # skip headers (if necessary)
    next(reader)

    # pull relevant data from CSV. edit this section to match the format of your CSV file
    proposals = []
    for row in reader:
        proposal = {
            "title": row[0],
            "description": row[1],
            "url": row[2],
        }
        proposals.append(proposal)

    # arrange proposals in alphabetical order (if necessary)
    proposals.sort(key=lambda p: p['title'].split(' -- ')[1])

    # create the event payload. customize your event data below
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "event_title": "My Event Title",
        "event_description": "",
        "num_voters": 10,
        "credits_per_voter": 99,
        "start_event_date": "2022-04-13T17:00:00.057Z",
        "end_event_date": "2022-04-14T23:00:00.057Z",
        "subjects": proposals,
    }
    url = 'https://quadraticvote.radicalxchange.org' if not dev else 'http://localhost:' + port
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
