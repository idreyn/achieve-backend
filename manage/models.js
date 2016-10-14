// This is a difference Question than the one in quiz/
class Question extends Model {
	constructor(id,text,choices,index,correct,explanation) {
		this.id = id;
		this.text = text;
		this.choices = choices;
		this.index = index;
		this.correct = correct;
		this.explanation = explanation;
	}
}