output = replicate.run(
    "camenduru/tripo-sr:be2a9b2b50937a3cc770ff9981881515f40393f9c66914bbd5db84ffca6a32fc",
    input={
        "image_path": img_file,
        "do_remove_background": remove_bg,
        "foreground_ratio": foreground_ratio
    }
)
