class FindOutOneOut:

    def __init__(self):
        pass

    #####################
    # Description:
    #   Reduce the inputted data to obtain a data set that shows the odd one out
    # Input:
    #   @param data: A list of dictionary structures containing information about items
    # Output:
    #   An array [reduced data, list of items]
    #####################
    def odd_one_out(self, data):
        if data is None:
            raise TypeError

        all_titles = []
        for i in data:
            all_titles.append(i['title'])

        try:
            intersecting_data = self.get_intersections(data)
            minimized_data = self.remove_overlapping_categories(intersecting_data)
        except IndexError:
            print("Problem sorting data. Please try a different input. Exiting program...")
            exit()
        return [minimized_data, all_titles]

    #####################
    # Description:
    #
    # Input:
    #   @param data: A list of dictionary structures containing information about items
    # Output:
    #
    #####################
    @staticmethod
    def get_intersections(data):
        output_data = []
        if data is None:
            raise TypeError

        for i in range(len(data)):
            end = len(data) + i - 1

            # Gets all combinations of possible sets
            if end > len(data):
                data_set = data[i:] + data[:end - len(data)]
            else:
                data_set = data[i:end]

            output_titles = []

            # Find which combination of possible sets provides common categories by using intersection
            common_categories = data_set[0]['categories'][:]
            output_titles.append(data_set[0]['title'])
            for x in range(1, len(data_set)):
                title = data_set[x]['title']
                category_set = data_set[x]['categories']
                output_titles.append(title)
                common_categories = list(set(common_categories) & set(category_set))

            output_data.append({
                'titles': output_titles,
                'common_categories': common_categories
            })

        return output_data

    #####################
    # Description:
    #   Remove all categories that overlap over all items
    # Input:
    #   @param data: A list of dictionary structures containing information about items
    # Output:
    #   The same data inputted, but with some data removed
    #####################
    @staticmethod
    def remove_overlapping_categories(data):
        if data is None:
            raise TypeError
        # Get overlapping categories
        overlapping_categories = data[0]['common_categories']
        for i in data[1:]:
            common_categories = i['common_categories']
            overlapping_categories = list(set(overlapping_categories) & set(common_categories))

        if len(overlapping_categories) > 0:
            print("Removed " + str(len(overlapping_categories)) + " items from all categories due to all having the same duplicates.")

        # Remove overlapping categories from original data input
        for i in data:
            common_categories = i['common_categories']
            for a_category in overlapping_categories:
                if a_category in common_categories:
                    common_categories.remove(a_category)

        return data
