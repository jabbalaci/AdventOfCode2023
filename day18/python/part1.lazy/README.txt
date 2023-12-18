Lazy method for Part 1
======================

* The program `part1.py` produces the file `example.pbm`.
* Open `example.pbm` in Gimp and fill the are.
  See `before.jpg` and `after.jpg`.
* Export the image in PBM format in ASCII mode.
  See `example-filled.pbm`.
* Count the number of 1s to get the area of the polygon.

    $ cat example-filled.pbm | tail -n +4 | tr -d 0 | tr -d '\n' | wc -c
    62

Now do the same steps with the real input.
