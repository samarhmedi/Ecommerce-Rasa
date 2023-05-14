import json

file_path = 'actions/products.json'

with open(file_path, 'r') as file:
    for line in file:
        try:
            product_data = json.loads(line)
            product_name = product_data['name']
            product_permalink = product_data['permalink']
            print(f"Product name: {product_name}")
            print(f"Product link: {product_permalink}")
            print("---------------")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON on line: {line}")
            print(f"Error details: {e}")
        except KeyError as e:
            print(f"Error: 'name' or 'permalink' key not found in JSON object: {product_data}")
            print(f"Error details: {e}")

def product_exists(product_name):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                product_data = json.loads(line)
                if product_data['name'].lower() == product_name.lower():
                    return True
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line}")
                print(f"Error details: {e}")
            except KeyError as e:
                print(f"Error: 'name' key not found in JSON object: {product_data}")
                print(f"Error details: {e}")
    return False



def recommend_similar_products(product_name):
    # A function to find similar products based on your criteria.
    # This is a simple example using string matching, but you can improve it using more advanced techniques like NLP.
    recommended_products = []
    max_recommended = 3
    with open(file_path, 'r') as file:
        for line in file:
            try:
                product_data = json.loads(line)
                if product_name.lower() in product_data['name'].lower():
                    recommended_product = {
                        'name': product_data['name'],
                        'permalink': product_data['permalink']
                    }
                    recommended_products.append(recommended_product)
                    if len(recommended_products) >= max_recommended:
                        break
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line}")
                print(f"Error details: {e}")
            except KeyError as e:
                print(f"Error: 'name' or 'permalink' key not found in JSON object: {product_data}")
                print(f"Error details: {e}")
    return recommended_products



product_name = "CHOCOLAT "
recommended_products = recommend_similar_products(product_name)

print(f"Recommended products for '{product_name}':")
for product in recommended_products:
    print(f"Product name: {product['name']}")
    print(f"Product link: {product['permalink']}")
    print("---------------")

product_name = "MIEL DE THYM"
exists = product_exists(product_name)

print(f"Does the product '{product_name}' exist? {exists}")
