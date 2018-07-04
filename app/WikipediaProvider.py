import requests


class WikipediaProvider:
    category_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=categories&redirects&cllimit=max&clshow=!hidden&titles="
    links_url = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=links&pllimit=max&titles="

    def __init__(self):
        return

    #####################
    # Description:
    #   Obtain data from an online endpoint
    # Input:
    #   @param url: A string representing an endpoint
    #   @param array_input: A list of strings to append to url
    # Output:
    #   Returns false if there was a problem with obtaining the data, otherwise it returns the data in a JSON format
    #####################
    def _get_page_data(self, url, array_input):
        titles = ""
        for i in array_input:
            titles += i.replace(' ', '_') + "|"
        titles = titles[0:-1]

        try:
            response = requests.get(url + titles)
            return response.json()['query']
        except Exception as e:
            print("Error connecting to the endpoint. Please check your connection.")
            exit()

    #####################
    # Description:
    #   Obtain all links on a Wikipedia page
    # Input:
    #   @param title: a string representing a page on Wikipedia
    # Output:
    #   Returns a list of links on a Wikipedia page
    #####################
    def _get_page_links(self, title):
        possible_alternatives = []
        data = self._get_page_data(self.links_url, [title])['pages']

        if 'links' not in data[next(iter(data))]:
            raise KeyError

        # For each link inside the page
        for i in data[next(iter(data))]['links']:
            possible_alternatives.append(i['title'])

        return possible_alternatives

    #####################
    # Description:
    #   For a list of inputs, get categories for each item
    # Input:
    #   @param array_input: a list of items to get data on
    # Output:
    #   Returns A list that contains dictionaries describing each item with an associated categories
    #####################
    def first_search(self, array_input):
        # Check inputs
        if len(array_input) == 0 or array_input is None:
            raise TypeError

        output = []

        data = self._get_page_data(self.category_url, array_input)
        page_data = data['pages']

        if 'redirects' in data:
            print("Certain pages have been redirected automatically. Changes can be seen below:")
            for redirect_data in data['redirects']:
                print("\tFrom: '" + redirect_data['from'] + "' To: '" + redirect_data['to'] + "'")

        # For each page
        for page in page_data:
            # Title of each page i.e. 'Running'
            title = page_data[page]['title']

            list_of_categories = []
            output_page_data = {
                'title': title,
                'missing_page': False,
                'ambiguous_page': False,
                'ambiguous_page_data': None,
                'categories': list_of_categories
            }
            categories = []
            # Will throw KeyError if Category returns 'missing'
            try:
                categories = page_data[page]['categories']
            except KeyError:
                output_page_data['missing_page'] = True
                output_page_data['missing_page_data'] = title

            # Each category in a title
            for category in categories:
                # Check if Disambiguation
                if categories[0]['title'] == "Category:Disambiguation pages":
                    output_page_data['ambiguous_page'] = True
                    try:
                        output_page_data['ambiguous_page_data'] = self._get_page_links(title)
                    except KeyError:
                        print("Program could not obtain necessary data from servers. Exiting now.")
                        exit()
                else:
                    list_of_categories.append(category['title'])

            output.append(output_page_data)
        return output

    #####################
    # Description:
    #   For a list of inputs, get data on categories for each item
    # Input:
    #   @param depth_range: An integer representing how many times to search recursively
    #   @param data_in: A list of dictionaries that represent items with categories
    # Output:
    #   Returns A formatted list of data containing new updated lists of categories
    #####################
    def get_depth_categories(self, depth_range, data_in):
        if not depth_range.isdigit() or data_in is None or depth_range is None:
            raise TypeError

        expanding_data = []
        expanding_data_index = []
        for data in data_in:
            if 'categories' not in data or 'title' not in data:
                raise KeyError
            expanding_data.append(data['categories'])
            expanding_data_index.append(data['title'])

        to_search = data_in[:]

        for depth in range(int(depth_range)):
            string_of_titles = ''

            # Get list of titles
            list_of_titles = []
            for i in to_search:
                list_of_titles += i['categories'] 

            # Obtain data
            current_data = self._get_page_data(self.category_url, list_of_titles)['pages']
            to_search = []

            # Clean up data
            for z in current_data:
                # Remove unnecessary data obtained from Wikipedia
                current_data[z].pop('pageid')
                current_data[z].pop('ns')

                # Restructure data
                tmp_array = []
                for x in current_data[z]['categories']:
                    tmp_array.append(x['title'])

                current_data[z]['categories'] = tmp_array[:]

                title = current_data[z]['title']
                category_data = current_data[z]['categories']

                # Add found data back into data_in
                for a_category in expanding_data:
                    if title in a_category:
                        for j in category_data:
                            if j not in a_category:
                                a_category.append(j)

                # Data to search for next iteration
                to_search.append(current_data[z])
        return data_in
