"""
Group Information:
Rojae Wedderburn: UWI ID:620146963
Hackerrank Username: rojaewedderburn

Member 2: N/A
"""
################################################## Global Variables ####################################################

knownPassengers = {}
fare = 1
passenger_list = []  # contains a list of passenger information requesting a taxi
# Each passenger information is a string with Telephone Number, Location, and Destination separated by spaces.

########################################################################################################################

# PART 1
def driver_construct(lastName, firstName, address, carMakeAndModel):
    """Constructor-Makes a new driver"""
    return ('Driver', [lastName, firstName, address, carMakeAndModel, 0, 0])


def getDriverInfo(driver):
    """"Accessor-Returns all the info of a particular driver"""
    return driver[1]


def driver_getLastName(driver):
    """"Accessor-Returns the last name of a particular driver"""
    return getDriverInfo(driver)[0]


def driver_getFirstName(driver):
    """"Accessor-Returns the first name of a particular driver"""
    return getDriverInfo(driver)[1]


def driver_getAddress(driver):
    """"Accessor-Returns the address of a particular driver"""
    return getDriverInfo(driver)[2]


def driver_getCarMakeAndModel(driver):
    """"Accessor-Returns the car make and model of a particular driver's car"""
    return getDriverInfo(driver)[3]


def driver_getNumberOfTripsCompleted(driver):
    """"Accessor-Returns the number of completed trips by particular driver"""
    return getDriverInfo(driver)[4]


def driver_getNumberOfPassengersTransported(driver):
    """"Accessor-Returns the number of passengers a particular driver has transported"""
    return getDriverInfo(driver)[5]


def driver_increaseTripsCompleted(driver):
    """Mutator-Increases the number of trips completed by a driver by 1"""
    getDriverInfo(driver)[4] += 1


def driver_increasePassengersTransported(driver, passengers):
    """Mutator-Increases the number of passengers transported by a driver"""
    getDriverInfo(driver)[5] += passengers


def driver_isNewDriver(driver):
    """Predicate- Determines if a driver is new based on their number of completed trips; 0 trips=new driver"""
    return driver_getNumberOfTripsCompleted(driver) == 0


# PART 2
def getAvailabilityQueue(LocationName):
    """Returns an availability queue from the list of availability queues based on the given location name """
    for availabilityQueue in availabilityQueue_LIST:
        if availabilityQueue_getLocationName(availabilityQueue) == LocationName:
            return availabilityQueue


def availabilityQueue_make(locationName):
    """Constructor- Makes an availability queue for drivers available at a particular location"""
    return ('AvailablityQueue', locationName, [])


def availabilityQueue_getLocationName(availabilityQueue):
    """Accessor -Returns location for a given availability queue"""
    return availabilityQueue[1]


def aQueueContents(availabilityQueue):
    """Accessor -Returns all drivers of the given availability queue in a list"""
    return availabilityQueue[2]


def availabilityQueue_front(availabilityQueue):
    """Accessor-Returns the driver at the front of the queue where the front of the queue is assigned to index 0"""
    return aQueueContents(availabilityQueue)[0]


def availabilityQueue_enqueue(availabilityQueue, driver):
    """Mutator-Adds a driver to the back of the availability queue; last index of the list"""
    aQueueContents(availabilityQueue).append(driver)


def availabilityQueue_dequeue(availabilityQueue):
    """Mutator-Removes driver at the front of the availability queue"""
    aQueueContents(availabilityQueue).pop(0)


def availabilityQueue_isEmpty(availabilityQueue):
    """Predicate-Determines if the given availability queue is empty"""
    return aQueueContents(availabilityQueue) == []


# PART 3
###################################### Availability Queues From Different Locations ##################################
availabilityQueue_UWI = availabilityQueue_make("UWI")
availabilityQueue_Papine = availabilityQueue_make("Papine")
availabilityQueue_Liguanea = availabilityQueue_make("Liguanea")
availabilityQueue_HalfWayTree = availabilityQueue_make("Half-Way-Tree")
availabilityQueue_DownTownKgn = availabilityQueue_make("DownTown-Kingston")
########################################################################################################################
availabilityQueue_LIST = [availabilityQueue_UWI, availabilityQueue_Papine, availabilityQueue_Liguanea,\
                          availabilityQueue_HalfWayTree, availabilityQueue_DownTownKgn]


########################################################################################################################


# PART 4
def calculateDiscount(passengerTelephoneNumber):
    """Calculates the discount a passenger should receive"""
    # passenger not liable for discount if they are not in dictionary -> knownPassengers
    if passengerTelephoneNumber not in knownPassengers:
        return 0.0
    return 0.10 * knownPassengers[passengerTelephoneNumber] * fare
    # base discount is 10% for 1 failed taxi request
    # It increases by a factor of the number of failed taxi requests for  a known passenger


# PART 5
def calculateFare(startLocation, endLocation, passengerTelephoneNumber):
    """Calculates the fare for a passenger"""
    discount = calculateDiscount(passengerTelephoneNumber)
    return fare - discount


# PART 6
def moveTaxi(startLocation, endLocation, passengers):
    """Moves a taxi from one location to another. Also increases number of trips and passengers for the taxi moved"""
    taxi = ''
    start_availability_q = getAvailabilityQueue(startLocation)
    end_availability_q = getAvailabilityQueue(endLocation)
    if not availabilityQueue_isEmpty(start_availability_q):
        taxi = availabilityQueue_front(start_availability_q)
        availabilityQueue_dequeue(start_availability_q)
        availabilityQueue_enqueue(end_availability_q, taxi)
        driver_increaseTripsCompleted(taxi)
        driver_increasePassengersTransported(taxi, passengers)
    else:
        return "No Drivers Available"


# PART 7
def requestTaxi(passengerTelephoneNumber, passengers, passengerLocation, passengerDestination):
    if passengerLocation == passengerDestination:
        return "LocationError: Your location and destination must be different areas"
    print(calculateFare(passengerLocation, passengerDestination, passengerTelephoneNumber))
    continue_trip = (input('Enter "Y" to confirm the trip or "N" to cancel -')).upper()
    if continue_trip == 'N':
        return "See you next time"
    elif continue_trip == 'Y':
        for availability_queue in availabilityQueue_LIST:
            if passengerLocation == availabilityQueue_getLocationName(availability_queue):
                if aQueueContents(availability_queue) == []:  # if no drivers are available and...
                    if passengerTelephoneNumber in knownPassengers:
                        # if passenger is known then their failed attempts will increase by 1
                        knownPassengers[passengerTelephoneNumber] += 1
                        print("No driver available")
                    else:  # if the passenger is not known and no drivers are available then...
                        # ...they will be added to knownPassengers with number of failed attempts initialized to 1
                        knownPassengers[passengerTelephoneNumber] = 1  # This would prevent a key error
                        print("No driver available")
                else:
                    # if there is a taxi currently available then it will be moved by the moveTaxi function to a new
                    # location
                    moveTaxi(passengerLocation, passengerDestination, passengers)
                    break
            else:
                pass
    else:
        # In case the passenger gives a response other than 'N' or 'Y'
        return "Invalid response. Try again."


# PART 8
def umts_main():
    request = input("")
    n = -1
    while request == 'Y':
        # A while loop is used because we do not know how many requests each passenger will make
        # Therefore the loop will terminate once they wish to stop making requests
        n += 1  # used as index to get access to each passenger information in passenger_list
        passenger = passenger_list[n].split()
        passengerTelephoneNumber = int(passenger[0])
        passengerLocation = passenger[1]
        passengerDestination = passenger[2]
        passengers = int(passenger[3])
        requestTaxi(passengerTelephoneNumber, passengers, passengerLocation, passengerDestination)
        request = input()  # Notice the request variable can toggle between 'Y' and 'N' in the sequence of the loop
        # If not done then the loop would run indefinitely until the computer memory is exhausted
    print()
    print()
    print('List of Drivers and Number of Jobs Completed :')
    for availabilityQueue in availabilityQueue_LIST:
        for driver in aQueueContents(availabilityQueue):
            print(driver_getFirstName(driver) + ' ' + driver_getLastName(driver) + ' ' + \
                  str(driver_getNumberOfTripsCompleted(driver)))
    print()
    print('List of Locations and Priority Driver :')
    for availabilityQueue in availabilityQueue_LIST:
        if not availabilityQueue_isEmpty(availabilityQueue):
            driver = availabilityQueue_front(availabilityQueue)
            print(availabilityQueue_getLocationName(availabilityQueue) + ' - ' + \
                  driver_getFirstName(driver) + \
                  ' ' + driver_getLastName(driver) + ' ' + driver_getCarMakeAndModel(driver))
        else:
            continue

umts_main()
