convert_heic(){
    # iterate over the arguments 
    for arg in "$@"
    do
        heic-to-jpg --keep -s $arg
    done
}