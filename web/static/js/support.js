function LatitidueFormatter(pos) {
	return PositionFormatter(pos, "N", "S");
}
function LongitudeFormatter(pos) {
	return PositionFormatter(pos, "E", "W");
}

function PositionFormatter(pos, posSymbol, negSymbol) {
	if (!isNumeric(pos))
		return pos;
	var isNegative = (pos < 0);
	if (isNegative) pos = -pos;
	var p1 = Math.floor(pos);
	var p2 = ((pos - (Math.floor(pos))) * 60).toFixed(2);
	return p1 + "&deg; " + p2 + " " + (isNegative ? negSymbol : posSymbol);
}

function EnterExitFormatter(entered) {
	return entered ? "Entered" : "Exited";
}

function TimeSpanFormatter(spanSeconds) {
	if (spanSeconds == 0)
		return "-";
	var s = "";
	var days = Math.floor(spanSeconds / 3600 / 24);
	if (days > 0) {
		s = (days > 1 ? days + " days, " : "1 day, ");
		spanSeconds -= days * 3600 * 24;
	}
	var hours = Math.floor(spanSeconds / 3600);
	spanSeconds -= hours * 3600;
	var minutes = Math.floor(spanSeconds / 60);
	var seconds = Math.floor((spanSeconds - 60 * minutes) / 60);
	if ((s.length > 0) || (hours > 0))
		return s + hours + "h " + minutes +"m";
	else
		return minutes + "m " + seconds + "s"
}

function DistanceFormatter(distance) {
	if (distance == 0)
		return "-";
	if (distance < 0.5) {
		return (distance * 1852).toFixed(0) + " m";
	} else if (distance < 100) {
		return distance.toFixed(1) + " nm";
	} else
		return distance.toFixed(0) + " nm";
}

dateTimeReviver = function (key, value) {
	var a;
	debugger;
	if (typeof value === 'string') {
		a = /\/Date\((\d*)\)\//.exec(value);
		if (a) {
			return new Date(+a[1]);
		}
	}
	return value;
}

function twoDigit(n) {
	return n > 9 ? "" + n : "0" + n;
}

function DateTimeFormatter(time) {
	var start = time.indexOf("(");
	var end = time.indexOf(")");
	if ((start == -1) || (end == -1))
		return "-";

	var v = time.substring(start + 1, end) * 1.0;
	var dt = new Date(v);
	return dt.getDate() + "/" + (dt.getMonth() + 1) + ", " + twoDigit(dt.getHours()) + ":" + twoDigit(dt.getMinutes());
}
	


function DisableMe(e) {
	e.disabled = true;
	return true;
}

function isNumeric(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}
