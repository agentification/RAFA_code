

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a d)
(ontable b)
(on c g)
(on d c)
(on e b)
(ontable f)
(on g e)
(on h a)
(ontable i)
(clear f)
(clear h)
(clear i)
)
(:goal
(and
(on a b)
(on b c)
(on c g)
(on e h)
(on f a)
(on h d)
(on i f))
)
)


