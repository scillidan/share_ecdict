# share_ecdict

[![Create Releases](https://github.com/scillidan/share_ecdict/actions/workflows/releases.yml/badge.svg)](https://github.com/scillidan/share_ecdict/actions/workflows/releases.yml)

Data from [ECDICT-ultimate](https://github.com/skywind3000/ECDICT-ultimate), extracted by [dict-ecdict](https://github.com/tuberry/dict-ecdict). See more on [ECDICT](https://github.com/skywind3000/ECDICT).

## Usage

1. Download files from [Releases](https://github.com/scillidan/share_ecdict/releases).
2. Use them in GoldenDict (StarDict format), sdcv, dictd.
3. See preview screenshot [here](asset/).

### sdcv

```sh
sdcv --color --use-dict ECDICT -n <word>
```

### dictd

```sh
# Arch
unzip ecdict-<version>-dictd.zip
sudo cp ecdict-<version>-dictd.{index,dict.dz} /usr/share/dictd/
sudo vim /etc/dict/dictd.conf
```

```
# Add database
database ecdict {
	data /usr/share/dictd/ecdict-<version>-dictd.dict.dz
	index /usr/share/dictd/ecdict-<version>-dictd.index
}
```

```sh
sudo systemctl restart dictd.service
```

```sh
dict --host localhost --port 2528 --database ecdict <word>
```