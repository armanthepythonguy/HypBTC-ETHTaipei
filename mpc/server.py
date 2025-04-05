from flask import Flask, request, jsonify
import random
app = Flask(__name__)

P = 2**127-1

def share_secret(value: int) -> [int]:
    """Split a secret into 3 shares using additive secret sharing."""
    s1 = random.randint(0, P - 1)
    s2 = random.randint(0, P - 1)
    s3 = (value - s1 - s2) % P
    return [s1, s2, s3]

@app.route('/secret_share/<num>', methods=['GET'])
def secret_share_api(num):
    shares = share_secret(int(num))
    e = [5,11,13]
    n = 8363630155366286024234552788761714985222139
    shares = [pow(shares[i],e[i],n) for i in range(3)]
    return jsonify(shares)

if __name__ == '__main__':
    app.run(debug=True)