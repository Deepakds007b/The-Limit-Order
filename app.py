from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
date = datetime.now()
with open("config.json", 'r') as c:
    value = json.load(c)

app = Flask(__name__)
# app.config['UPLOAD_FOLDER']= value['upload_location']


@app.route('/')
def home():
    return render_template("layout.html")


def buy_sell(size, radio, filename):
    counter=0
    z = filename+str("_share")
    if(radio=="Buy" and int(size)>int(value[z])):
        counter=1
        return counter
    if(radio == "Buy" and int(size)<=int(value[z])):
        a = int(value[z])
        b = int(size)
        c = a-b
        value[z] = c
        with open("config.json", 'w') as f:
            json.dump(value, f)
    elif(radio == "Sell"):
        a = int(value[z])
        b = int(size)
        c = a+b
        value[z] = c
        with open("config.json", 'w') as f:
            json.dump(value, f)
    else:
        return redirect('/limitorder')

@app.route('/limitorder/buying', methods=['GET', 'POST'])
def buying():
    if (request.method == 'POST'):
        entered_price = request.form.get('price')
        entered_size = request.form.get('size')
        if(entered_size==""):
            return redirect('/LimitOrder')
        radio_value = request.form.get('a', False)
        if(entered_price == value['amazon_price']):
            a=buy_sell(entered_size, radio_value, "amazon")
        elif(entered_price == value['google_price']):
            a=buy_sell(entered_size, radio_value, "google")
        elif(entered_price == value['apple_price']):
            a=buy_sell(entered_size, radio_value, "apple")
        elif(entered_price == value['facebook_price']):
            a=buy_sell(entered_size, radio_value, "facebook")
        elif(entered_price == value['microsoft_price']):
            a=buy_sell(entered_size, radio_value, "microsoft")
        elif(entered_price == value['netflix_price']):
            a=buy_sell(entered_size, radio_value, "netflix")
        elif(entered_price == value['jio_price']):
            a=buy_sell(entered_size, radio_value, "jio")
        elif(entered_price == value['flipkart_price']):
            a=buy_sell(entered_size, radio_value, "flipkart")
        elif(entered_price == value['walmart_price']):
            a=buy_sell(entered_size, radio_value, "walmart")
        elif(entered_price == value['airtel_price']):
            a=buy_sell(entered_size, radio_value, "airtel")
        else:
            return redirect("/LimitOrder")
    
    return render_template("LimitOrder.html",date=date,counter=a,value=value,entered_price=entered_price,entered_size=entered_size,radio_value=radio_value)

@app.route('/ordershow')
def ordershow():
    return render_template("ordershow.html", date=date,value=value)


@app.route('/orderbook', methods=['GET', 'POST'])
def orderbook():
    return render_template("orderbook.html", date=date, value=value)


@app.route('/MarketOrder', methods=['GET', 'POST'])
def MarketOrder():    
    return render_template("MarketOrder.html", date=date, value=value)


@app.route('/marketorder/buying', methods=['GET', 'POST'])
def MarketOrderbuying():
    if(request.method == 'POST'):
        entered_size = request.form.get('size')
        radio_value = request.form.get('a', False)
        if(radio_value == "Buy"):
            if(int(entered_size)<=int(value['microsoft_share'])):
                buy_sell(entered_size,radio_value,"microsoft")
            elif(int(entered_size)>int(value['microsoft_share'])):
                c= int(entered_size)-int(value['microsoft_share'])
                if(c<=int(value['facebook_share'])):
                    buy_sell(value['microsoft_share'],radio_value,"microsoft")
                    buy_sell(c,radio_value,"facebook")
                elif(c>int(value["facebook_share"])):
                    d=c-int(value["facebook_share"])
                    if(d<=int(value['apple_share'])):
                        buy_sell(value['microsoft_share'],radio_value,"microsoft")
                        buy_sell(value["facebook_share"],radio_value,"facebook")
                        buy_sell(d,radio_value,"apple")
                    elif(d>int(value['apple_share'])):
                        e=d-int(value['apple_share'])
                        if(e<=int(value['google_share'])):
                            buy_sell(value['microsoft_share'],radio_value,"microsoft")
                            buy_sell(value["facebook_share"],radio_value,"facebook")
                            buy_sell(value['apple_share'],radio_value,"apple")
                            buy_sell(e,radio_value,"google")
                        elif(e>int(value['google_share'])):
                            f=e-int(value['google_share'])
                            if(f<=int(value["amazon_share"])):
                                buy_sell(value['microsoft_share'],radio_value,"microsoft")
                                buy_sell(value["facebook_share"],radio_value,"facebook")
                                buy_sell(value['apple_share'],radio_value,"apple")
                                buy_sell(value['google_share'],radio_value,"google")
                                buy_sell(f,radio_value,"amazon")
                            elif(f>int(value['amazon_share'])):
                                return redirect('/MarketOrder')
        elif(radio_value=="Sell"):
            if(int(entered_size)<=int(value['netflix_share'])):
                buy_sell(entered_size,"Buy","netflix")
            elif(int(entered_size)>int(value['netflix_share'])):
                c= int(entered_size)-int(value['netflix_share'])
                if(c<=int(value['jio_share'])):
                    buy_sell(value['netflix_share'],"Buy","netflix")
                    buy_sell(c,"Buy","jio")
                elif(c>int(value["jio_share"])):
                    d=c-int(value["jio_share"])
                    if(d<=int(value['flipkart_share'])):
                        buy_sell(value['jio_share'],"Buy","netflix")
                        buy_sell(value["jio_share"],"Buy","jio")
                        buy_sell(d,"Buy","flipkart")
                    elif(d>int(value['flipkart_share'])):
                        e=d-int(value['flipkart_share'])
                        if(e<=int(value['walmart_share'])):
                            buy_sell(value['netflix_share'],"Buy","netflix")
                            buy_sell(value["jio_share"],"Buy","jio")
                            buy_sell(value['flipkart_share'],"Buy","flipkart")
                            buy_sell(e,"Buy","walmart")
                        elif(e>int(value['walmart_share'])):
                            f=e-int(value['walmart_share'])
                            if(f<=int(value["airtel_share"])):
                                buy_sell(value['netflix_share'],"Buy","netflix")
                                buy_sell(value["jio_share"],"Buy","jio")
                                buy_sell(value['flipkart_share'],"Buy","flipkart")
                                buy_sell(value['walmart_share'],"Buy","walmart")
                                buy_sell(f,"Buy","airtel")
                            elif(f>int(value['airtel_share'])):
                                return redirect('/MarketOrder')

    return render_template("MarketOrder.html", date=date, value=value)


@app.route('/LimitOrder', methods=['GET', 'POST'])
def limitorder():
    return render_template("LimitOrder.html", date=date, value=value)


if __name__ == "__main__":
    app.run(debug=True)
