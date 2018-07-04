from WikipediaProvider import WikipediaProvider
from FindOddOneOut import *


class Driver:
    def __init__(self):
        print('Find the odd one out\n')

        input_array, depth = self.get_inputs()
        wiki_provider = WikipediaProvider()
        odd_out_provider = FindOutOneOut()

        first_search_data = wiki_provider.first_search(input_array)

        validate_input_details = self.validate_input(first_search_data)

        # If input is not valid
        if not validate_input_details[0]:
            print("Due to no information being found for:")
            for title in validate_input_details[1]:
                print("\t" + title)
            print("The program can not proceed. Please check spelling and whether such inputs exist as pages on Wikipedia.")
            exit(0)

        # If input is valid, but ambiguous, retrieve data again
        if validate_input_details[1] is not None:
            first_search_data = wiki_provider.first_search(validate_input_details[1])

        # If all data is good to go, remove redundant data i.e. missing_page
        finalized_input_data = []
        for i in first_search_data:
            finalized_input_data.append({
                'title': i['title'],
                'categories': i['categories']
            })

        try:
            found_data = wiki_provider.get_depth_categories(depth, finalized_input_data)
        except TypeError:
            print("Incorrect search depth inputted Program exiting.")
            exit()
        except KeyError:
            print("Problem with obtaining correct data. Program exiting.")
            exit()

        # Analyse results
        results = odd_out_provider.odd_one_out(found_data)

        # Display results
        self.display_results(results)

    #####################
    # Description:
    #   Checks if input exists on Wikipedia, or if input is ambiguous. If Ambiguous, the user will be prompted to input
    #   an alternative answer
    # Input:
    #   @param first_search_data: A list of dictionary structures containing information about items
    # Output:
    #   An array [true if data is valid false otherwise, first_search_data fixed up]
    #####################
    @staticmethod
    def validate_input(first_search_data):
        if first_search_data is None:
            raise TypeError

        valid_input_data = True
        missing_data = []
        research_data = []

        # Check if any inputs did not return data
        for i in first_search_data:
            if 'missing_page' not in i or 'ambiguous_page' not in i:
                return [False, []]

            # Obtain list of missing pages (if any) to display to user
            if i['missing_page']:
                missing_data.append(i['missing_page_data'])
                valid_input_data = False

        # No point continuing as inputted data is invalid
        if not valid_input_data:
            return [False, missing_data]

        # Fix ambiguous inputs if any
        for i in first_search_data:
            title = i['title']
            page_data = i['ambiguous_page_data']

            # Obtain alternative input if ambiguous page found
            if i['ambiguous_page']:
                page_data.remove('Help:Disambiguation')
                print("\nAmbiguous input found for: " + title)
                print("Possible alternatives:\n\t-1. EXIT PROGRAM")
                for index, j in enumerate(page_data):
                    print("\t" + str(index) + ". " + j)

                alternative_num = None
                while alternative_num not in range(len(page_data)):
                    try:
                        alternative_num = int(input("Please input a number relating to an alternative item: "))
                        if alternative_num == -1:
                            print("Exiting program...")
                            exit()
                    except ValueError:
                        print("Invalid input.")

                print("You have replaced '" + title + "' with '" + page_data[alternative_num] + "'\n")
                title = page_data[alternative_num]

            research_data.append(title)

        return [True, research_data]

    #####################
    # Description:
    #   Receive inputs from users
    #
    # Return:
    #   A list in the format of [inputted items as a list, search depth]
    #####################
    @staticmethod
    def get_inputs():
        num_inputs = input('Number of inputs: ')
        while not num_inputs.isdigit() or int(num_inputs) < 3 or int(num_inputs) > 19:
            num_inputs = input('Please put a valid integer greater than 2 and less than 20: ')

        input_array = []
        for i in range(int(num_inputs)):
            input_array.append(str(input('Argument ' + str(i) + ': ')))

        depth_input = input('How deep to search? (Recommended 2): ')
        while not depth_input.isdigit() or int(depth_input) < 1 or int(depth_input) > 10:
            depth_input = input('Please put a valid integer between 1 and 10: ')

        return [input_array, depth_input]

    #####################
    # Description:
    #   Display results from the FindOddOneOut module
    # Input:
    #   @param data: A list of size 2, the first index containing a list of dictionaries describing each item, the
    #                second containing a list original inputted items
    #####################
    def display_results(self, data):
        if data is None:
            raise TypeError

        input_data = data[0]
        all_titles = data[1]

        curr_max = 0
        curr_max_data = []
        curr_data = None

        for each_data in input_data:
            common_categories = each_data['common_categories']
            titles = each_data['titles']

            print("-------------------------------------------------")
            print("For inputted items:")
            for title in titles:
                print("\t" + title)

            if len(common_categories) != 0:
                print("There were " + str(len(common_categories)) + " common categorie(s) found. Seen below.")
                for i in common_categories:
                    if i[0:9] == "Category:":
                        print("\t" + i[9:])
                    else:
                        print("\t" + i)

                if len(common_categories) > curr_max:
                    curr_max = len(common_categories)
                    curr_max_data.clear()
                    curr_max_data.append(each_data)
                    curr_data = each_data
                elif len(common_categories) == curr_max:
                    curr_max_data.append(each_data)
            else:
                print("There were no unique common categories found.")
        print("-------------------------------------------------\n")

        print("Out of items:")
        for i in all_titles:
            print("\t" + i)
        print()
        if curr_max == 0:
            print('No unique common factors found to differentiate between items. Try a higher depth if necessary.')
        else:
            if len(curr_max_data) > 1:
                print('The most probable odd one out is: ' + str(list(set(all_titles) - set(curr_data['titles']))[0]))
            else:
                print('The most probable odd one out is: ' + str(list(set(all_titles) - set(curr_data['titles']))[0]))

if __name__ == "__main__":
    Driver()
