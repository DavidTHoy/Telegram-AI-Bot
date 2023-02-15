from bs4 import BeautifulSoup


def get_request_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }


def get_data_from_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    data = ' '.join([s.get_text(strip=True) for s in soup.findAll('p')])
    return data


def add_html_formatting(summ_list):
    """
    Add some html formatting for displaying in telegram a bit nicer
    :param summ_list:
    :return:
    """
    if not summ_list:
        return "Unable to parse!"
    for cnt, el in enumerate(summ_list):
        summ_list[cnt] = '<pre> &#8226; ' + summ_list[cnt] + '</pre>\n'
    return ' '.join(summ_list)


def split_text(text):
    """
    This method will split the text into a batch size that a model with 1024 tokens can handle
    :param text:
    :return:
    """
    all_text = []
    for i in range(int(len(text) / 4500)):
        if not len(text[i * 4500:i * 4500 + 4500]) > 1000:
            continue
        else:
            all_text.append(text[i * 4500:i * 4500 + 4500])
    return all_text
