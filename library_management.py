from flask import Flask,request,jsonify,redirect,url_for
import sqlite3

app=Flask(__name__)

def db_connection():

    conn=None

    conn=sqlite3.connect("library1.db")

    return conn

@app.route("/book_library",methods=["GET"])

def books_get():

    conn=db_connection()

    cursor=conn.cursor()

    if request.method == "GET":

        cursor.execute("""SELECT * from book_data""")
        

        books_list=[
                   {
                   'book_name':row[0],
                   'book_id':row[1],
                   'author':row[2],
                   'status':row[3],
                   'category':row[4]
                   }
                   for row in cursor.fetchall()]

        cursor.close()

        conn.close()

        return jsonify(books_list)

    

@app.route("/book_library",methods=["POST"])

def books_register():

    conn=db_connection()

    cursor=conn.cursor()

    if request.method=="POST":

        book_name=request.form['book_name']
        book_id=request.form['book_id']
        author=request.form['author']
        status=request.form['status']
        category=request.form['category']
        
        query="""INSERT INTO book_data(book_name,book_id,author,status,category)
               VALUES(?,?,?,?,?)"""
        
        cursor.execute(query,(book_name,book_id,author,status,category))

        book_created={
                      'book_name':book_name,
                      'book_id':book_id,
                      'author':author,
                      'status':status,
                      'category':category
                     }

        conn.commit()

        print("book with id {} is registered".format(book_id))

        cursor.close()

        conn.close()
        
        return jsonify(book_created)


@app.route("/book_library/<int:id>",methods=["GET"])

def book_issue(id):

    conn=db_connection()

    cursor=conn.cursor()

    if request.method=="GET":

        query="""SELECT book_id from book_data where book_id=?"""

        cursor.execute(query,(id,))

        id_status=cursor.fetchone()

        if id_status is not None:

            print("book with id {} is present in data".format(id))

            query="""SELECT status from book_data where book_id=?"""

            cursor.execute(query,(id,))

            result=cursor.fetchone()

            book_status=result[0]

            if book_status=="available":

                print("book with id {} is available to issue".format(id))
                
                res=input("do u want to issue book y/n:")

                if res=='y':
                    
                    query="""UPDATE book_data SET status='issued'
                             WHERE book_id=?"""

                    cursor.execute(query,(id,))

                    conn.commit()

                    print("book with id {} is issued".format(id))


                return "book status of book id {} is updated and book is issued".format(id)


            else:
                return "book with given id {} is already issued".format(id)

        else:
            return "given id does not exist"

    cursor.close()
    conn.close()

@app.route("/book_library/<int:id>",methods=["DELETE"])

def book_delete(id):

    conn=db_connection()

    cursor=conn.cursor()

    if request.method=="DELETE":

        get_status="""SELECT status from book_data where book_id=?"""

        cursor.execute(get_status,(id,))

        result=cursor.fetchone()

        res=result[0]

        print(res)

        if res=="available":

            query="""DELETE FROM book_data where book_id=?"""

            cursor.execute(query,(id,))

            conn.commit()

            cursor.close()

            conn.close()


            return "the book with book_id {} deleted".format(id)
        
    conn.commit()

    cursor.close()
    conn.close()


    return "book with given id is not available , it is issued"
    


@app.route("/book_library/<int:id>",methods=["PUT"])

def book_update(id):

    conn=db_connection()

    cursor=conn.cursor()
    
    if request.method=="PUT":
        
        book_name=request.form['book_name']
        author=request.form['author']
        status=request.form['status']
        category=request.form['category']
        

        query="""UPDATE book_data SET
                 book_name=?,
                 author=?,
                 status=?,
                 category=?
                 WHERE book_id=?"""

        cursor.execute(query,(book_name,author,status,category,id))
        
        conn.commit()
        
    cursor.close()
    conn.close()

    return "book is updated with book id {}".format(id)


@app.route("/book_library/<int:id>",methods=["PATCH"])

def book_status_update(id):

    conn=db_connection()

    cursor=conn.cursor()
    
    if request.method=="PATCH":

        status=request.form['status']
        
        query="""UPDATE book_data SET
                 status=?
                 WHERE book_id=?"""

        cursor.execute(query,(status,id))
        
        conn.commit()
        
    cursor.close()
    
    conn.close()

    return "book status of book id {} is updated ".format(id)




@app.route("/book_library",methods=["GET"])

def book12():

    conn=db_connection()

    cursor=conn.cursor()

    if request.method=="GET":

        book_id=request.args.get('book_id')
        
        if book_id:
            query="""SELECT * from book_data where book_id=? """

        cursor.execute(query,(book_id))

        books_list=[
                   {
                   'book_name':row[0],
                   'book_id':row[1],
                   'author':row[2],
                   'status':row[3],
                   'category':row[4]
                   }
                   for row in cursor.fetchall()]

    cursor.close()
    
    conn.close()

    return jsonify(books_list)


            

if __name__=="__main__":

    app.run(debug=True)
