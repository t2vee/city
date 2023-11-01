import json

payload = '''{"track": {"_id": "64a7d930f52ef3ef57a24aba", "album": "7pZA63LsjuRCziMYfjEYjf",
                     "artists": ["0BYEp3eyHK9Wsp4t2Ad1R8"],
                     "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ",
                                           "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU",
                                           "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO",
                                           "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR",
                                           "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA",
                                           "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS",
                                           "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR",
                                           "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ",
                                           "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT",
                                           "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW",
                                           "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL",
                                           "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ",
                                           "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ",
                                           "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE",
                                           "ET", "XK"], "disc_number": 1, "duration_ms": 185266, "explicit": false,
                     "external_ids": {"isrc": "DK4BB9901002"},
                     "external_urls": {"spotify": "https://open.spotify.com/track/13i5XpzqdQ5KTIKatuIVoa"},
                     "href": "https://api.spotify.com/v1/tracks/13i5XpzqdQ5KTIKatuIVoa", "id": "13i5XpzqdQ5KTIKatuIVoa",
                     "is_local": false, "name": "The Sailor Song", "popularity": 43,
                     "preview_url": "https://p.scdn.co/mp3-preview/d1a54c6e4ca0ad661bad2a412b0dc7e39f75fe5d?cid=560194af726a42c0b47e83e689f3bba6",
                     "track_number": 2, "type": "track", "uri": "spotify:track:13i5XpzqdQ5KTIKatuIVoa", "__v": 0},
           "artist": {"_id": "64a7d933f52ef3ef57a24b09",
                      "external_urls": {"spotify": "https://open.spotify.com/artist/0BYEp3eyHK9Wsp4t2Ad1R8"},
                      "followers": {"href": null, "total": 50171}, "genres": ["bubblegum dance", "eurodance"],
                      "href": "https://api.spotify.com/v1/artists/0BYEp3eyHK9Wsp4t2Ad1R8",
                      "id": "0BYEp3eyHK9Wsp4t2Ad1R8", "images": [
                   {"height": 1000, "url": "https://i.scdn.co/image/f5fa6c70f10c4cb37ed7f1ecb3d62c87fe0f6fbe",
                    "width": 1000},
                   {"height": 640, "url": "https://i.scdn.co/image/4cca3caba269ae28b285e448142214aa2515db95",
                    "width": 640},
                   {"height": 200, "url": "https://i.scdn.co/image/ee924cf704ac8cbf2a5ef22d2b81ade49d892552",
                    "width": 200},
                   {"height": 64, "url": "https://i.scdn.co/image/f2f3704fb34c9e1736bde68d6e0fae3235d97916",
                    "width": 64}], "name": "Toy-Box", "popularity": 46, "type": "artist",
                      "uri": "spotify:artist:0BYEp3eyHK9Wsp4t2Ad1R8", "__v": 0},
           "album": {"_id": "64a7d932f52ef3ef57a24ae3", "album_type": "album", "artists": ["0BYEp3eyHK9Wsp4t2Ad1R8"],
                     "available_markets": ["AD", "AE", "AG", "AL", "AM", "AO", "AR", "AT", "AU", "AZ", "BA", "BB", "BD",
                                           "BE", "BF", "BG", "BH", "BI", "BJ", "BN", "BO", "BR", "BS", "BT", "BW", "BY",
                                           "BZ", "CA", "CD", "CG", "CH", "CI", "CL", "CM", "CO", "CR", "CV", "CW", "CY",
                                           "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "ES", "ET", "FI",
                                           "FJ", "FM", "FR", "GA", "GB", "GD", "GE", "GH", "GM", "GN", "GQ", "GR", "GT",
                                           "GW", "GY", "HK", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IN", "IQ", "IS",
                                           "IT", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KR", "KW", "KZ",
                                           "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC",
                                           "MD", "ME", "MG", "MH", "MK", "ML", "MN", "MO", "MR", "MT", "MU", "MV", "MW",
                                           "MX", "MY", "MZ", "NA", "NE", "NG", "NI", "NL", "NO", "NP", "NR", "NZ", "OM",
                                           "PA", "PE", "PG", "PH", "PK", "PL", "PS", "PT", "PW", "PY", "QA", "RO", "RS",
                                           "RW", "SA", "SB", "SC", "SE", "SG", "SI", "SK", "SL", "SM", "SN", "SR", "ST",
                                           "SV", "SZ", "TD", "TG", "TH", "TJ", "TL", "TN", "TO", "TR", "TT", "TV", "TW",
                                           "TZ", "UA", "UG", "US", "UY", "UZ", "VC", "VE", "VN", "VU", "WS", "XK", "ZA",
                                           "ZM", "ZW"], "copyrights": [
                   {"text": "1999 Spin Music! Distributed by Playground Music Scandinavia AB", "type": "C"},
                   {"text": "1999 Spin Music! Distributed by Playground Music Scandinavia AB", "type": "P"}],
                     "external_ids": {"upc": "7332181020205"},
                     "external_urls": {"spotify": "https://open.spotify.com/album/7pZA63LsjuRCziMYfjEYjf"},
                     "genres": [], "href": "https://api.spotify.com/v1/albums/7pZA63LsjuRCziMYfjEYjf",
                     "id": "7pZA63LsjuRCziMYfjEYjf", "images": [
                   {"height": 640, "url": "https://i.scdn.co/image/ab67616d0000b273217ad0d06bdf511798990acb",
                    "width": 640},
                   {"height": 300, "url": "https://i.scdn.co/image/ab67616d00001e02217ad0d06bdf511798990acb",
                    "width": 300},
                   {"height": 64, "url": "https://i.scdn.co/image/ab67616d00004851217ad0d06bdf511798990acb",
                    "width": 64}], "name": "FanTastic", "popularity": 52, "release_date": "1999-01-01",
                     "release_date_precision": "day", "type": "album", "uri": "spotify:album:7pZA63LsjuRCziMYfjEYjf",
                     "__v": 0}, "bestPeriod": [{"_id": {"year": 2023, "month": 8}, "count": 107, "total": 699},
                                               {"_id": {"year": 2020, "month": 6}, "count": 92, "total": 699}],
           "firstLast": {"_id": null, "first": {"_id": "64bc833dbdb2b08b1e5cf6a4", "owner": "64a7d5e3f52ef3ef57a243de",
                                                "id": "13i5XpzqdQ5KTIKatuIVoa", "played_at": "2019-12-04T11:11:36.000Z",
                                                "__v": 0},
                         "last": {"_id": "654136a50385293126876b19", "owner": "64a7d5e3f52ef3ef57a243de",
                                  "id": "13i5XpzqdQ5KTIKatuIVoa", "played_at": "2023-10-31T17:14:47.154Z", "__v": 0}},
           "recentHistory": [
               {"_id": "654136a50385293126876b19", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T17:14:47.154Z", "__v": 0},
               {"_id": "654136a50385293126876b1a", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T17:11:45.486Z", "__v": 0},
               {"_id": "654136a50385293126876b1b", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T17:08:39.489Z", "__v": 0},
               {"_id": "654136a50385293126876b17", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T17:05:34.471Z", "__v": 0},
               {"_id": "654136a50385293126876b18", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T17:02:28.488Z", "__v": 0},
               {"_id": "654132b50385293126876ac5", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T16:59:22.490Z", "__v": 0},
               {"_id": "654132b50385293126876ac6", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T16:56:16.488Z", "__v": 0},
               {"_id": "654132b50385293126876ac1", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T16:53:11.488Z", "__v": 0},
               {"_id": "654132b50385293126876ac2", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T16:50:05.466Z", "__v": 0},
               {"_id": "654132b50385293126876ac3", "owner": "64a7d5e3f52ef3ef57a243de", "id": "13i5XpzqdQ5KTIKatuIVoa",
                "played_at": "2023-10-31T16:46:59.472Z", "__v": 0}], "total": {"count": 699}}'''


def clean_spotify_stat_payload_track(data):
    simplified_data = {}

    # Extracting relevant data from 'track'
    track = data.get("track", {})
    simplified_data["track_id"] = track.get("_id")
    simplified_data["track_name"] = track.get("name")
    simplified_data["track_album_id"] = track.get("album")
    simplified_data["track_artists"] = track.get("artists")
    simplified_data["track_popularity"] = track.get("popularity")

    # Extracting relevant data from 'artist'
    artist = data.get("artist", {})
    simplified_data["artist_id"] = artist.get("_id")
    simplified_data["artist_name"] = artist.get("name")
    simplified_data["artist_genres"] = artist.get("genres")

    # Extracting relevant data from 'album'
    album = data.get("album", {})
    simplified_data["album_id"] = album.get("_id")
    simplified_data["album_name"] = album.get("name")
    simplified_data["album_popularity"] = album.get("popularity")
    best_period = data.get("bestPeriod", {})
    simplified_data["best_period"] = best_period

    # Extracting relevant data from 'firstLast'
    first_last = data.get("firstLast", {})
    simplified_data["first_played"] = first_last.get("first", {}).get("played_at")
    simplified_data["last_played"] = first_last.get("last", {}).get("played_at")

    # Extracting relevant data from 'total'
    total = data.get("total", {})
    simplified_data["total_count"] = total.get("count")

    return json.dumps(simplified_data)


print(clean_spotify_stat_payload_track(json.loads(payload)))

data = {"track_id": "64a7d930f52ef3ef57a24aba", "track_name": "The Sailor Song",
        "track_album_id": "7pZA63LsjuRCziMYfjEYjf", "track_artists": ["0BYEp3eyHK9Wsp4t2Ad1R8"], "track_popularity": 43,
        "artist_id": "64a7d933f52ef3ef57a24b09", "artist_name": "Toy-Box",
        "artist_genres": ["bubblegum dance", "eurodance"], "album_id": "64a7d932f52ef3ef57a24ae3",
        "album_name": "FanTastic", "album_popularity": 52,
        "best_period": [{"_id": {"year": 2023, "month": 8}, "count": 107, "total": 716},
                        {"_id": {"year": 2020, "month": 6}, "count": 92, "total": 716}],
        "first_played": "2019-12-04T11:11:36.000Z", "last_played": "2023-11-01T17:40:53.494Z", "total_count": 716}
