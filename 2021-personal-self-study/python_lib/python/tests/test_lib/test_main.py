import test_lib.main as main

def test_main1():
    output = main.quadratic_func(4)
    
    if output == 16:
        result = True
    else:
        result = False
    
    assert result == True

def test_main2():
    output = main.quadratic_func(3)
    
    if output == 9:
        result = True
    else:
        result = False

    assert result == False