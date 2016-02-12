%#template to generate html table from a list of tuples
<p>The open items are as follows:</p>
<table border="1">
    % for row in rows:
    <tr>
        % for col in row:
        <td>{{col}}</td>
        % end
    </tr>
    % end
</table>